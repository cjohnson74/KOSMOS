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


class ManeuverAgent:
    def __init__(self, model_name="gpt-4o", temperature=0, top_k_vals=5, timeout_period=120, checkpoint_dir="checkpoint", resume=1):
        print(f"🔍 DEBUG: ManeuverAgent initializing with model={model_name}, top_k={top_k_vals}, resume={resume}")
        
        try:
            self.llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.7,
                openai_api_key=api_key  
            )
            print(f"🔍 DEBUG: ManeuverAgent LLM initialized successfully")
            f_mkdir(f"{checkpoint_dir}/skill/code")
            f_mkdir(f"{checkpoint_dir}/skill/description")
            f_mkdir(f"{checkpoint_dir}/skill/chroma_db")
            self.control_primitives = []  # Empty list for testing without control primitives
            # if resuming from checkpoint
            if resume: # make it so that it runs
                print(f'🔍 DEBUG: ManeuverAgent loading from checkpoint {checkpoint_dir}/skill')
                try:
                    self.availablemaneuvers = load_json(f"{checkpoint_dir}/skill/available_maneuvers.json")
                    print(f"🔍 DEBUG: ManeuverAgent loaded {len(self.availablemaneuvers)} maneuvers from checkpoint")
                except Exception as e:
                    print(f"🔍 ERROR: ManeuverAgent failed to load checkpoint: {e}")
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
        # passed in dictionary from kosmos.py, add import
        code_function_name = data["code_function_name"]
        code_function_body = data["code_function_body"]
        print(f"🔍 DEBUG: ManeuverAgent function name: '{code_function_name}', body length: {len(code_function_body)} chars")

        maneuver_overview = self.createDescription(code_function_name, code_function_body)
        # test if reached here
        print(f"🔍 DEBUG: ManeuverAgent maneuver overview created: {maneuver_overview[:200]}...")

        # check if code function name is not in the available skills list
        if code_function_name not in self.availablemaneuvers:
            print(f"🔍 DEBUG: ManeuverAgent adding new maneuver '{code_function_name}'")
            dumped_function_name = code_function_name
            try:
                self.vector_db.add_texts(
                texts=[maneuver_overview],
                ids=[code_function_name],
                metadatas=[{"name": code_function_name}]
            )
            except Exception as e:
                print(f"🔍 ERROR: ManeuverAgent error adding text to vector DB: {e}")
                return

            # appending a new maneuver to dictionary of maneuvers
            self.availablemaneuvers[code_function_name] = {
                "code" : code_function_body,
                "description" : maneuver_overview
            }
            print(f"🔍 DEBUG: ManeuverAgent maneuver '{code_function_name}' added to available maneuvers\n {self.availablemaneuvers[code_function_name]}")

            # dump code and text for newly added maneuvers

            # in .txt
            dump_text(
                maneuver_overview,
                f"{self.checkpoint_dir}/skill/description/{dumped_function_name}.txt"
            )

            # in .py
            dump_text(
                code_function_body,
                f"{self.checkpoint_dir}/skill/code/{dumped_function_name}.py"
            )
            # in .json
            dump_json(
                self.availablemaneuvers,
                f"{self.checkpoint_dir}/skill/available_maneuvers.json"
            )


     

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

        maneuvers = []

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
