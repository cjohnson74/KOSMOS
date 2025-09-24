import ast
import re
import time

import kosmos.utils as U
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from langchain.prompts import AIMessage, HumanMessage, SystemMessage

from kosmos.prompts import load_prompt
from kosmos.control_primitives_context import load_control_primitives_context

class FlightAgent:
    def __init__(
        self,
        model_name="gpt-4o",
        temperature=0,
        request_timeout=120,
        checkpoint_dir="checkpoint",
        chat_log=True,
        execution_error=True,
    ):
        self.checkpoint_dir = checkpoint_dir
        self.chat_log = chat_log
        self.execution_error = execution_error
        U.f_mkdir(f"{checkpoint_dir}/action")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )

    def construct_system_message(self, skills=[]):
        system_template = load_prompt("action_template")
        base_skills = [
            # load control primitives
        ]
        programs = "\n\n".join(load_control_primitives_context(base_skills) + skills)
        response_format = load_prompt("action_response_format")
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template
        )
        system_message = system_message_prompt.format(
            programs=programs, response_format=response_format
        )
        assert isinstance(system_message, SystemMessage)
        return system_message

    def construct_human_message(self, *, events, code="", task="", context="", audit=""):
        chat_messages = []
        error_messages = []
        assert events[-1][0] == "observe", "Last event must be observe"
        for i, (event_type, event) in enumerate(events):
            # Process events here - placeholder for now
            pass

        observation = ""

        if code:
            observation += f"Code from the last round:\n{code}\n\n"
        else:
            observation += f"Code from the last round: No code in the first round\n\n"
        
        if self.execution_error:
            if error_messages:
                error = "\n".join(error_messages)
                observation += f"Execution error:\n{error}\n\n"
            else:
                observation += f"Execution error: No error\n\n"

        if self.chat_log:
            if chat_messages:
                chat_log = "\n".join(chat_messages)
                observation += f"Chat log: {chat_log}\n\n"
            else:
                observation += f"Chat log: None\n\n"

        # FIXME: add all the game telemetry to the observation

        observation += f"Task: {task}\n\n"

        if context:
            observation += f"Context: {context}\n\n"
        else:
            observation += f"Context: None\n\n"

        if audit:
            observation += f"Audit: {audit}\n\n"
        else:
            observation += f"Critique: None\n\n"

        return HumanMessage(content=observation)

    def process_ai_message(self, message):
        assert isinstance(message, AIMessage)

        retry = 3
        error = None
        while retry > 0:
            try:
                code_pattern = re.compile(r"```(?:python|py)(.*?)```", re.DOTALL)
                code = "\n".join(code_pattern.findall(message.content))
                parsed = ast.parse(code)
                functions = []
                assert len(parsed.body) > 0, "No functions found"
                
                for node in parsed.body:
                    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    
                    node_type = "AsyncFunctionDef" if isinstance(node, ast.AsyncFunctionDef) else "FunctionDef"
                    
                    # Extract function parameters
                    params = []
                    for arg in node.args.args:
                        params.append(arg.arg)
                    
                    # Get function source code (simplified - in practice you might want to use ast.unparse)
                    functions.append({
                        "name": node.id.name,
                        "type": node_type,
                        "body": ast.unparse(node),
                        "params": params,
                    })
                
                # Find the last async function
                main_function = None
                for function in reversed(functions):
                    if function["type"] == "AsyncFunctionDef":
                        main_function = function
                        break
                
                assert (
                    main_function is not None
                ), "No async function found. Your main function must be async."
                assert (
                    len(main_function["params"]) == 1
                    and main_function["params"][0] == "bot"
                ), f"Main function {main_function['name']} must take a single argument named 'bot'"
                
                program_code = "\n\n".join(function["body"] for function in functions)
                exec_code = f"await {main_function['name']}(bot)"
                
                return {
                    "program_code": program_code,
                    "program_name": main_function["name"],
                    "exec_code": exec_code,
                }
            except Exception as e:
                retry -= 1
                error = e
                time.sleep(1)
        return f"Error parsing action response (before program execution): {error}"

    def summarize_chatlog(self, events):
        chatlog = set()
        for event_type, event in events:
            if event_type == "onChat":
                chatlog.add(event["onChat"])
        return "I also need " + ", ".join(chatlog) + "." if chatlog else ""