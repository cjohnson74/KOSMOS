import os
from kosmos.utils import f_mkdir, load_json, dump_text, dump_json
from kosmos.prompts import load_prompt
# from kosmos.control_primitives import load_control_primitives  # Disabled for testing
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file


api_key = os.getenv('OPENAI')

# database to store successful code
vector_db = []

# Dummy code for KRPC docking automation
docking_code = '''
def dock_with_target():

    # This script assumes the vessel is next to the target and the target is a ship.
    conn = krpc.connect(name="Docking with target")
    sc = conn.space_center
    mj = conn.mech_jeb
    active = sc.active_vessel

    # Set the first docking port as the controlling part
    print("Setting the first docking port as the controlling part")
    parts = active.parts
    parts.controlling = parts.docking_ports[0].part

    # Find a free docking port attached to the target vessel and set it as the target
    print("Looking for a free docking port attached to the target vessel")
    for dp in sc.target_vessel.parts.docking_ports:
        if not dp.docked_part:
            sc.target_docking_port = dp
            break

    # Engage Docking Autopilot and close the connection when it finishes
    print("Starting the docking process")
    docking = mj.docking_autopilot
    docking.enabled = True

    with conn.stream(getattr, docking, "enabled") as enabled:
        enabled.rate = 1  # we don't need a high throughput rate, 1 second is more than enough
        with enabled.condition:
            while enabled():
                enabled.wait()

    print("Docking complete!")
    conn.close()
'''
class ManeuverAgent:
    def __init__(self, model_name="gpt-4o", temperature=0, top_k_vals=5, timeout_period=120, checkpoint_dir="checkpoint", resume=0):
        print(f"🔍 DEBUG: ManeuverAgent initializing with model={model_name}, top_k={top_k_vals}, resume={resume}")
        
        # Correct way to create an LLM object for the llm parameter
        try:
            # Option 1: Using OpenAI (requires API key)
            self.llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.7,
                openai_api_key=api_key  
            )
            print(f"🔍 DEBUG: ManeuverAgent LLM initialized successfully")
            f_mkdir(f"{checkpoint_dir}/skill/code")
            f_mkdir(f"{checkpoint_dir}/skill/description")
            f_mkdir(f"{checkpoint_dir}/skill/chroma_db")
            # primitives for env
            # self.control_primitives = load_control_primitives()  # Disabled for testing
            self.control_primitives = []  # Empty list for testing without control primitives
            # if resuming from checkpoint
            if resume:
                print(f'🔍 DEBUG: ManeuverAgent loading from checkpoint {checkpoint_dir}/skill')
                self.availablemaneuvers = load_json(f"{checkpoint_dir}/skill/available_maneuvers.json")
                print(f"🔍 DEBUG: ManeuverAgent loaded {len(self.availablemaneuvers)} maneuvers from checkpoint")
            else:
                # dictionary for maneuvers (function names + descriptions)
                self.availablemaneuvers = {}
                print(f"🔍 DEBUG: ManeuverAgent starting fresh with no maneuvers")

            # k vals for nearest neighbor search
            self.top_k_vals = top_k_vals

            self.checkpoint_dir = checkpoint_dir
            
            print("🔍 DEBUG: ManeuverAgent initialized successfully!")
            try:
            # Open the Chroma vector store
                self.vector_db = Chroma(
                    collection_name="code_descriptions",
                    persist_directory="./KOSMOS/skill/chroma_db",
                    embedding_function=OpenAIEmbeddings(openai_api_key=api_key)
                    )
                print(f"🔍 DEBUG: ManeuverAgent vector store opened successfully with {self.vector_db._collection.count()} documents")
            except Exception as e:
                print(f"🔍 ERROR: ManeuverAgent error opening vector store: {e}")
        except Exception as e:
            print(f"🔍 ERROR: ManeuverAgent error initializing: {e}")
            print("Make sure you have the correct LangChain version and API keys set up")
            self.agent = None

        assert self.vector_db._collection.count() == len(self.availablemaneuvers), (
            f"Skill Manager's vectordb is not synced with skills.json.\n"
            f"There are {self.vector_db._collection.count()} skills in vectordb but {len(self.availablemaneuvers)} skills in skills.json.\n"
            f"Did you set resume=False when initializing the manager?\n"
            f"You may need to manually delete the vectordb directory for running from scratch."
        )

    @property
    def programs(self):
        programs = ""
        # Handle both dict and list formats for availablemaneuvers
        if isinstance(self.availablemaneuvers, dict):
            for maneuver_name, entry in self.availablemaneuvers.items():
                programs += f"{entry['code']}\n\n"
        elif isinstance(self.availablemaneuvers, list):
            for entry in self.availablemaneuvers:
                if isinstance(entry, dict) and 'code' in entry:
                    programs += f"{entry['code']}\n\n"
        for primitives in self.control_primitives:
            programs += f"{primitives}\n\n"
        return programs

    # function to add a skill
    def add_new_maneuver(self, data):
        print(f"🔍 DEBUG: ManeuverAgent adding new maneuver with data keys: {list(data.keys())}")
        print(f"🔍 DEBUG: ManeuverAgent data type: {type(data)}")
        print(f"🔍 DEBUG: ManeuverAgent checking for 'program_name' key...")
        
        # TESTING -- see if the key exists in data hashmap
        if "program_name" not in data:
            print(f"🔍 ERROR: ManeuverAgent 'program_name' key missing!")
            print(f"🔍 ERROR: Available keys: {list(data.keys())}")
            print(f"🔍 ERROR: Data contents: {data}")
            return
        else:
            print(f"🔍 DEBUG: ManeuverAgent 'program_name' key found successfully")
            # passed in dictionary from kosmos.py, add import
            code_function_name = data["program_name"]
        code_function_body = data["program_code"]
        print(f"🔍 DEBUG: ManeuverAgent function name: '{code_function_name}', body length: {len(code_function_body)} chars")

        maneuver_overview = self.createDescription(code_function_name, code_function_body)
        # test if reached here
        print(f"🔍 DEBUG: ManeuverAgent maneuver overview created: {maneuver_overview[:200]}...")

        # check if code function name is not in the available skills list
        if code_function_name not in self.availablemaneuvers:
            written_function_name = code_function_name
            print(f"🔍 DEBUG: ManeuverAgent adding new maneuver '{code_function_name}'")
        else:
            print(f"🔍 DEBUG: ManeuverAgent maneuver '{code_function_name}' already exists, creating new version")
            # delete the instance from vector db
            self.vector_db.delete(ids=[code_function_name])
            # since it's at least the 2nd version of the function
            i = 2
            # iterate through directory to increment counter and see how many copies as to dump in new instance
            while f"{code_function_name}V{i}.py" in os.listdir(f"{self.checkpoint_dir}/skill/code"):
                i += 1
            # have new version of function name
            written_function_name = (f"{code_function_name}V{i}")
            print(f"🔍 DEBUG: ManeuverAgent new maneuver version '{written_function_name}' created")

        # Add to vector database (for both new and existing maneuvers)
        self.vector_db.add_texts(
            texts=[maneuver_overview],
            ids=[code_function_name],
            metadatas=[{"name": written_function_name}]
        )

        # appending a new maneuver to dictionary of maneuvers
        self.availablemaneuvers[code_function_name] = {
            "code" : code_function_body,
            "description" : maneuver_overview
        }

        # dump code and text for newly added maneuvers

        # in .txt
        dump_text(
            maneuver_overview,
            f"{self.checkpoint_dir}/skill/description/{written_function_name}.txt"
        )

        # in .py
        dump_text(
            code_function_body,
            f"{self.checkpoint_dir}/skill/code/{written_function_name}.py"
        )

        dump_json(
            self.availablemaneuvers,
            f"{self.checkpoint_dir}/skill/available_maneuvers.json"
        )

        # make it persistent storage in vector db
        self.vector_db.persist()
        print(f"🔍 DEBUG: ManeuverAgent maneuver '{code_function_name}' saved successfully")

    def createDescription(self, code_function_name, code_function_body):
        print(f"🔍 DEBUG: ManeuverAgent creating description for function '{code_function_name}'")
        messages = [
            SystemMessage(content=load_prompt("maneuver")),
            HumanMessage(
                content=code_function_body + "\n\n" + f"The main function is '{code_function_name}'."
            )
        ]
        print(f"🔍 DEBUG: ManeuverAgent calling LLM to generate description")
        # overview of maneuver
        llm_response = self.llm(messages).content
        print(f"🔍 DEBUG: ManeuverAgent LLM response length: {len(llm_response)} chars")
        maneuver_overview = f"    // {llm_response}"

        result = f"async function {code_function_name}(bot) {{\n{maneuver_overview}\n}}"
        print(f"🔍 DEBUG: ManeuverAgent description created, length: {len(result)} chars")
        return result
        # invoke message to AI agent
        #agent_response = self.llm.invoke(messages)
        # for testing
        #print(agent_response)

        # if there was an actual description 
        #if agent_response:
        #    vector_db.append(agent_response)

    # retrieve maneuvers from vector db
    def getManeuvers(self, query):
        print(f"🔍 DEBUG: ManeuverAgent retrieving maneuvers for query: '{query[:100]}...'")
        num_results = min(self.vector_db._collection.count(), self.top_k_vals)
        print(f"🔍 DEBUG: ManeuverAgent vector DB has {self.vector_db._collection.count()} documents, requesting {num_results}")

        # if no near k values were found
        if num_results == 0:
            print(f"🔍 DEBUG: ManeuverAgent no maneuvers available in vector DB")
            return {}
        
        # prints number of expected k vals
        print(f"🔍 DEBUG: ManeuverAgent retrieving top {num_results} results for maneuvers")

        documents_and_scores = self.vector_db.similarity_search_with_score(query, k=num_results)
        print(f"🔍 DEBUG: ManeuverAgent found {len(documents_and_scores)} similar documents")
        print(
            "Documents retrieved:", f"{', '.join([doc.metadata['name'] for doc, score in documents_and_scores])}"
        )

        maneuvers = {}

        # iterate through the list of docs_and_scores as {keys: values}
        for doc, score in documents_and_scores:
            maneuver_name = doc.metadata["name"]
            print(f"🔍 DEBUG: ManeuverAgent processing maneuver '{maneuver_name}' with score {score:.3f}")
            if maneuver_name in self.availablemaneuvers:
                maneuvers.append(self.availablemaneuvers[maneuver_name]["code"])
            else:
                print(f"🔍 WARNING: ManeuverAgent maneuver '{maneuver_name}' not found in available maneuvers")

        print(f"🔍 DEBUG: ManeuverAgent returning {len(maneuvers)} maneuvers")
        return maneuvers