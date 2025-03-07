from crewai import Agent, Task, Crew
import os
os.environ['OPENAI_API_KEY'] = "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"

class CodeDocumenter:
    def __init__(self):
        print("Initializing...")
        self.agent = Agent(
            role="Code Documentation Generator",
            goal="Generate structured documentation from code files.",
            backstory="A smart AI that reads code and writes explanations for developers.",
            verbose=True
        )

    def read_code_file(self, file_path):
        print(f"Reading code file at path: {file_path}")
        if os.path.isfile(file_path) and file_path.endswith((".js", ".ts", ".jsx", ".tsx", ".py")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_name = os.path.basename(file_path)
                    file_content = f.read()
                    code_content = {file_name: file_content}
                    print(f"Successfully read file: {file_name}")
                    return code_content
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")
                return None
        else:
            if not os.path.isfile(file_path):
                print(f"No file found at {file_path}")
            else:
                print(f"File {file_path} is not a supported code file type.")
            return None

    def generate_documentation(self, folder_path):
        print("Generating documentation...")
        code_files = self.read_code_file(folder_path)
        print('code_files: ', code_files)

        documentation = {}
        task = Task(
            description=f"Generate documentation for the code file {code_files}",
            expected_output="Structured documentation explaining functions, components, and their usage.",
            agent=self.agent,
        )


        # for filename, code in code_files.items():
        #     task = Task(
        #         description=f"Generate documentation for the following code file:\n\n{code}",
        #         expected_output="Structured documentation explaining functions, components, and their usage.",
        #         agent=self.agent
        #     )
        #     tasks.append(task)

        # *Create Crew and execute tasks*
        crew = Crew(agents=[self.agent], tasks=[task])
        responses = crew.kickoff()  # Ensures execution

        # *Store output*
        for i, filename in enumerate(code_files.keys()):
            documentation[filename] = responses[i]

        return documentation


doc_generator = CodeDocumenter()
docs = doc_generator.generate_documentation("./TodoApp.jsx")
for file, doc in docs.items():
    print(f"### Documentation for {file}:\n{doc}\n")