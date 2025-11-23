# Understanding and Working with AI Agents
## A Hands-on Gen AI Workshop
## Session labs 
## Revision 1.2 - 08/26/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Lab 1 - Creating a simple agent**

**Purpose: In this lab, we’ll learn about the basics of agents and see how tools are called. We'll also see how Chain of Thought prompting works with LLMs and how we can have ReAct agents reason and act.**

---

**What the agent example does**
- Uses a local Ollama-served LLM (llama3.2) to interpret natural language queries about weather.
- Extracts coordinates from the input, queries Open-Meteo for weather data.
- Converts temperatures and provides a summary forecast using a TAO loop.

**What it demonstrates about the framework**
- Shows how to integrate **LangChain + Ollama** to drive LLM reasoning.
- Demonstrates **Chain of Thought** reasoning with `Thought → Action → Observation` steps.
- Introduces simple function/tool calling with a deterministic LLM interface.

--- 

### Steps

1. In our repository, we have a set of Python programs that we'll be building out to work with concepts in the labs. These are mostly in the *agents* subdirectory. Go to the *TERMINAL* tab in the bottom part of your codespace and change into that directory.
```
cd agents
```

2. For this lab, we have the outline of an agent in a file called *agent1.py* in that directory. You can take a look at the code either by clicking on [**agents/agent1.py**](./agents/agent1.py) or by entering the command below in the codespace's terminal.
   
```
code agent1.py
```

3. If you scroll through this file, you can see it outlines the steps the agent will go through without all the code. When you are done looking at it, close the file by clicking on the "X" in the tab at the top of the file.

4. Now, let's fill in the code. To keep things simple and avoid formatting/typing frustration, we already have the code in another file that we can merge into this one. Run the command below in the terminal.
```
code -d ../extra/lab1-code.txt agent1.py
```

5. Once you have run the command, you'll have a side-by-side view in your editor of the completed code and the agent1.py file.
  You can merge each section of code into the agent1.py file by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at the code, and then click to merge the changes in, one at a time.

![Side-by-side merge](./images/aa40.png?raw=true "Side-by-side merge") 

6. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/aa41.png?raw=true "Merge complete") 

7. Now you can run your agent with the following command:

```
python agent1.py
```

8. The agent will start running and will prompt for a location (or "exit" to finish). At the prompt, you can type in a location like "Paris, France" or "London" or "Raleigh" and hit *Enter*. After that you'll be able to see the Thought -> Action -> Observation loop in practice as each one is listed out. You'll also see the arguments being passed to the tools as they are called. Finally you should see a human-friendly message from the AI summarizing the weather forecast.

![Agent run](./images/aa42.png?raw=true "Agent run") 

9. You can then input another location and run the agent again or exit. Note that if you get a timeout error, the API may be limiting the number of accesses in a short period of time. You can usually just try again and it will work.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Leveraging Coding Agents and Persistence**

**Purpose: In this lab, we’ll see how agents can drive solutions via creating code and implementing simple memory techniques - using the smolagents framework.**

---

**What the agent example does**
- Uses SmolAgents to convert currencies and remember past conversions.
- Accepts incomplete input (e.g., “convert 200”) and fills in missing parts from memory.
- Stores memory in a local JSON file to persist state across sessions.

**What it demonstrates about the framework**
- Introduces the **SmolAgents CodeAgent**, a declarative and lightweight ReAct agent.
- Demonstrates **@tool decorators**, deterministic execution, and **tool chaining**.
- Highlights pluggable **memory support**, custom tools, and precise control over the agent loop.

---

### Steps

1. For this lab, we have a simple application that does currency conversion using prompts of the form "Convert 100 USD to EUR", where *USD* = US dollars and *EUR* = euros.  It will also remember previous values and invocations.


2. As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. The command to run this time is below:

```
code -d ../extra/curr_conv_agent.txt curr_conv_agent.py
```
</br></br>

![Code for memory agent](./images/aa68.png?raw=true "Code for memory agent") 

3. The code in this application showcases several SmolAgents features and agent techniques including the following. See how many you can identify as your reviewing the code.

- **@tool decorator** turns your Python functions into callable “tools” for the agent.  
- **LiteLLMModel** plugs in your local Ollama llama3.2 as the agent’s reasoning engine.  
- **CodeAgent** runs a ReAct loop: think (LLM), act (call tool), observe, repeat.  
- **Memory feature** remembers current values and persists them (with history) to an external JSON file.  


4. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent with the command below:

```
python curr_conv_agent.py
```

5. Enter a basic prompt like the one below.

```
Convert 100 USD to EUR
```

6. The agent will run for a while and not return as the LLM loads and the processing happens. When it is finished with this run, you'll see output like the screenshot below. Notice that since we used the SmolAgents CodeAgent type, you can see the code it created and executed in the black box. **NOTE: This initial run will take several minutes!** While you are waiting on it to complete, this is a good time to go back and look at the code in *curr_conv_agent.py* to understand more about it.

![Running agent](./images/aa69.png?raw=true "Running agent")   

7. Now you can try some partial inputs with missing values to demonstrate the agent remembering arguments that were passed to it before. Here are some to try. Output is shown in the screenshot. (You may see some intermediate steps. You're looking for the one with "Final answer" in it.)

```
Convert 200
Convert 400 to JPY
```

![Running with partial inputs](./images/aa70.png?raw=true "Running agent")  
![Running with partial inputs](./images/aa71.png?raw=true "Running agent")   


8. To see the stored history information on disk, type "exit" to exit the tool. Then in the terminal type the command below to see the contents of the file.

```
cat currency_memory.json
```

![Running with partial inputs](./images/aa72.png?raw=true "Running agent") 

9. Finally, you can start the agent again and enter "history" at the prompt to see the persisted history from before. Then you can try a query and it should pick up as before. In the example, we used the query below:

```
convert 300
```

![Running with partial inputs](./images/aa73.png?raw=true "Running agent")   


10.  Just type "exit" when ready to quit the tool.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

    
**Lab 3 - Using RAG with Agents - Enhanced with Memory and Context Awareness**

**Purpose: In this lab, we'll build an intelligent RAG agent that maintains conversation memory and handles follow-up questions**

---

**What the agent example does**
- Uses a proper three-step RAG pattern: **Retrieve → Augment → Generate**
- **Maintains conversation memory** across queries
- **Detects and handles follow-up questions** intelligently
- **Caches query results** for improved performance
- Augments prompts with both retrieved context and conversation history
- Provides source citations for transparency

**What makes this an AGENT (not just a RAG system)**
- **Conversation Memory**: Remembers last 3 exchanges for contextual understanding
- **Follow-up Detection**: Recognizes when you're asking about "that" or "it"
- **Smart Caching**: Reuses recent search results when appropriate
- **Contextual Responses**: Says "As we discussed earlier..." when referencing past answers
- **Stateful Interaction**: Unlike simple Q&A, maintains state across queries

---

### Steps

1. For this lab, we'll be using a comprehensive knowledge base of OmniTech company documentation including returns policies, device troubleshooting, shipping logistics, and account security. These PDFs are located in [**knowledge_base_pdfs/**](./knowledge_base_pdfs/)

2. First, we need to create the vector database from our PDFs. This will chunk the documents, create embeddings, and store them in ChromaDB. Change to the agents directory if you're not already there:

```
cd agents
```

3. Now run the indexing tool to create the vector database. This uses the same best practices from Day 1 including semantic chunking, table extraction, and rich metadata:

```
python ../tools/index_pdfs.py --pdf-dir ../knowledge_base_pdfs --chroma-path ./chroma_db
```

You should see output showing the PDFs being processed and chunks being indexed.

![Indexing PDFs](./images/rag-index.png?raw=true "Indexing PDFs")

4. As before, we'll use the "view differences and merge" technique to build our RAG agent. The updated code incorporates all the best practices including the three-step RAG pattern:

```
code -d ../extra/rag_agent.txt rag_agent.py
```
</br></br>

![Code for rag agent](./images/rag-code.png?raw=true "Code for rag agent")

Notice the three key methods in the code:
- `retrieve()` - Searches the vector database for relevant chunks
- `build_prompt()` - Augments the user query with retrieved context
- `generate()` - Calls the LLM to generate a grounded answer

5. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent:

```
python rag_agent.py
```

6. You'll see the agent connect to the ChromaDB database and display statistics about the knowledge base including total chunks and source documents. It will also check that Ollama is running with the correct model.

![RAG initialization](./images/rag-init.png?raw=true "RAG initialization")

7. The system will show example questions with follow-up suggestions. Notice the agent features like memory status and special commands. Try this conversation sequence:

**First question:**
```
How can I return a product?
```
The agent will provide a detailed answer with sources.

**Follow-up (demonstrating memory):**
```
Tell me more about the timeframe
```
Notice: The agent detects this as a follow-up and includes conversation context!

8. You'll see the agent's intelligence in action:
   - **[AGENT MEMORY]** messages when it detects follow-ups
   - **[RETRIEVE]** with caching (may say "Using cached results")
   - **Memory status** showing conversation length and cached queries
   - Contextual answers like "As we discussed earlier..."

![Agent memory in action](./images/rag-memory.png?raw=true "Agent memory in action")

9. Try another conversation thread to see memory handling:

```
What are the shipping costs?
```
Then follow with:
```
What about international?
```

The agent understands "international" refers to shipping without you saying "international shipping costs"!

10. Test the agent's special features:
   - Type `clear` to reset memory and start fresh
   - Ask about something NOT in docs: `What's the CEO's favorite color?`
   - Then go back to a previous topic: `What about returns?`
   - The agent will recall the earlier conversation!

11. After exploring, type `exit` to quit. The agent will show how many queries it processed.

**Key Takeaways - What Makes This an Agent:**
- **Memory & State**: Unlike simple RAG, this agent maintains conversation history
- **Context Awareness**: Detects and handles follow-up questions intelligently
- **Performance Optimization**: Caches queries to avoid redundant searches
- **Natural Conversation**: Understands pronouns and contextual references
- **Agent Behavior**: This is how agents differ from stateless Q&A systems - they remember, learn, and adapt within a session

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Working with multiple agents**

**Purpose: In this lab, we’ll see how to add an agent to a workflow using CrewAI.**

---

**What the agent example does**
- Implements a **CrewAI** workflow with multiple agents: travel, customer service, and booking.
- Coordinates task delegation between specialized agents.
- Simulates a flight booking process from information extraction to confirmation.

**What it demonstrates about the framework**
- Highlights **CrewAI’s structured multi-agent planning**, where each agent owns a role.
- Emphasizes **modularity**: clear division of responsibilities, reusable logic per agent.
- Demonstrates coordination, task assignment, and coherent multi-agent collaboration.

---

### Steps

1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/lab5-code.txt agent5.py
```

![Diffs](./images/aa23.png?raw=true "Diffs") 

2. In the *agent5.py* template, we have the imports and llm setup at the top filled in, along with a simulated function to book a flight. Scroll to the bottom. At the bottom is the input and code to kick off the "*crew*". So, we need to fill in the different tasks and setup the crew.

3. Scroll back to the top, review each change and then merge each one in. Notice the occurrences of "*booking_agent*". This is all being done with a single agent in the crew currently. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent5.py*.

![Merge complete](./images/aa24.png?raw=true "Merge complete") 

4. Now you can run the agent and see the larger workflow being handled. There will be quite a bit of output so this may take a while to run. **NOTE: Even though the agent may prompt for human input to select a flight, none is needed. We're not adding that in and using fake info to keep things simple and quick.**

```
python agent5.py
```

![Execution](./images/aa31.png?raw=true "Execution") 

5. Now, that we know how the code works and that it works, let's consider the overall approach. Since there are multiple functions going on here (getting info, finding flights, booking flights) it doesn't necessarily make sense to have just one agent doing all those things. Let's add two other agents - a *travel agent* to help with finding flights, and a customer_service_agent to help with user interactions. To start, open the code for editing.

```
code agent5.py
```


6. Now, replace the single *booking agent* definition with these definitions for the 3 agents (making sure to get the indenting correct):


**Directions:** Copy the block of replacement text in gray below and paste over the single agent definition in the code. Reminder - you may need to use keyboard shortcuts to copy and paste. The screenshots are only to show you before and after - they are not what you copy.

```
# Defines the AI agents

booking_agent = Agent(
    role="Airline Booking Assistant",
    goal="Help users book flights efficiently.",
    backstory="You are an expert airline booking assistant, providing the best booking options with clear information.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for travel planning tasks
travel_agent = Agent(
    role="Travel Assistant",
    goal="Assist in planning and organizing travel details.",
    backstory="You are skilled at planning and organizing travel itineraries efficiently.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for customer service tasks
customer_service_agent = Agent(
    role="Customer Service Representative",
    goal="Provide excellent customer service by handling user requests and presenting options.",
    backstory="You are skilled at providing customer support and ensuring user satisfaction.",
    verbose=True,
    llm=ollama_llm,
)
```
![Text to replace](./images/aa26.png?raw=true "Text to replace") 

![Replaced text](./images/aa27.png?raw=true "Replaced text")

7. Next, we'll change each *task definition* to reflect which agent should own it. The places to make the change are in the task definitions in the lines that start with "*agent=*". Just edit each one as needed per the mapping in the table below. The screenshot below the mappings shows what the changed code should look like.

| **Task** | *Agent* | 
| :--------- | :-------- | 
| **extract_travel_info_task** |  *customer_service_agent*  |        
| **find_flights_task** |  *travel_agent*  |  
| **present_flights_task** |  *customer_service_agent*  |  
| **book_flight_task** | *booking_agent* (ok as-is) |  
         
![Replaced text](./images/aa28.png?raw=true "Replaced text")

8. Finally, we need to add the new agents to our crew. Edit the "*agents=[*" line in the block under the comment "*# Create the crew*". In that line, add *customer_service_agent* and *travel_agent*. The full line is below. The screenshot shows the changes made.

```
agents=[booking_agent, customer_service_agent, travel_agent],
```

![Replaced text](./images/aa29.png?raw=true "Replaced text")

9. Now you can save your changes and then run the program again.

```
python agent5.py
```

10. This time when the code runs, you should see the different agents being used in the processing.

![Run with new agents](./images/aa30.png?raw=true "Run with new agents")

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 5 - Building Agents with the Reflective Pattern**

**Purpose: In this lab, we’ll see how to create an agent that uses the reflective pattern using the AutoGen framework.** 

---

**What the agent example does**
- Accepts a user request to generate Python code (e.g., “Plot a sine wave”).
- Uses a **code writer agent** to generate the initial response.
- Simulates execution of the generated code in a **sandboxed subprocess**, capturing any runtime output or errors.
- Passes the code (with runtime feedback) to a **critic agent** that assesses whether the code meets the original request.
- If the critic returns a `FAIL`, the code is passed to a **fixer agent** to revise it.
- Simulates execution of the **fixed code** as well and reports runtime behavior.
- Outputs either the original or revised code with a self-improvement cycle.

**What it demonstrates about the framework**
- Demonstrates **AutoGen’s modular agent design**, with roles like code writer, critic, and fixer.
- Uses **structured messaging** and system prompts to guide agent roles and ensure predictable output.
- Shows how to build **reflection patterns** with execution-aware feedback:  
  **generate → simulate → evaluate → revise → simulate**.
- Enhances LLM reliability by integrating **actual runtime behavior** into the critique loop.

---

### Steps


1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/reflect_agent.txt reflect_agent.py
```

![Diffs](./images/aip11.png?raw=true "Diffs") 

2. This time you'll be merging in the following sections:

- agent to write code
- agent to review code
- agent to fix code
- section to exec the code (note this only works if no additional imports are required)
- workflow sections to drive the agents

3. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent with the command below:

```
python reflect_agent.py
```

4. After the agent starts, you'll be at a prompt that says "Request >". This is waiting for you to input a programming request. Let's start with something simple like the prompt below. Just type this in and hit Enter.

```
determine if a number is prime or not
```

![Simple task](./images/aip6.png?raw=true "Simple task")

5. After this, you should see a "Generating Code..." message indicating the coding agent is generating code. Then you'll see the suggested code.

![Suggested code](./images/aip7.png?raw=true "Suggested code")

6. Next, you'll see where the agent tried to run the code and provides "Runtime Feedback" indicating whether or not it executed successfully. That's followed by the "Critique" and the PASS/FAIL verdict.

![Code evaluation](./images/aip8.png?raw=true "Code evaluation")
 
7. This one probably passed on the first round. The agent will be ready for another task. Let's see what it's like when there's an error. Try the following prompt:

```
Determine if a number is prime or not, but inject an error. Do not include a comment about the error.
```

8. After this runs, and the initial code is generated, you should see the "Critique" section noting this as a "FAIL". The agent will then attempt to automatically fix the code and suggest "Fixed Code". Then it will attempt to execute the fixed code it generated. If all goes well, you'll see a message after that indicating that the fixed code was "Executed successfully."

![Fix run](./images/aip9.png?raw=true "Fix run")

9. Let's try one more change. Use "*exit*" to stop the current agent. We have a version of the code that has some extra functionality built-in to stream output, print system_messages, show when an agent is running, etc. It's in the "extra" directory, under "reflect_agent_verbose.py". Go ahead and run that and try a prompt with it. You can try the same prompt as in step 7 if you want. (You can type "exit" to stop the running one.)

```
python ../extra/reflect_agent_verbose.py
```

![Verbose run](./images/aip10.png?raw=true "Verbose run")


10. (Optional) After this you can try other queries with the original file or the verbose one if you want. Or you can try changing some of the system messages in the code and re-running it if you like to try a larger change.


<p align="center">
**[END OF LAB]**
</p>
</br></br>


<p align="center">
**THANKS!**
</p>


