from flask import Flask, render_template, request, jsonify
import llm
import tools
import tool_schema
import system_prompt
import json
import inspect

app = Flask(__name__)

# This replaces the initial fresh start in your CLI version
# In a real app, you'd store this per-user session.
conversation_history = [{"role": "system", "content": system_prompt.get_receptionist_prompt()}]

@app.route('/')
def home():
    # Renders the HTML file (we will create this in the next step)
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # --- THE RECURSIVE AGENT LOOP (Integrated from your original code) ---
    while True:
        response = llm.get_completion(conversation_history, tool_schema.TOOLS)
        msg = response.choices[0].message

        has_content = bool(msg.content and msg.content.strip())
        has_tools = bool(msg.tool_calls)

        # CASE 1: AI wants to use tools
        if has_tools:
            conversation_history.append(msg)
            
            for tool in msg.tool_calls:
                name = tool.function.name
                try:
                    args = json.loads(tool.function.arguments)
                except:
                    args = {}

                # Data Mapping Fixes (from your original code)
                if "phone_number" in args: args["phone"] = args.pop("phone_number")
                if "email_address" in args: args["email"] = args.pop("email_address")

                print(f" [System: Accessing {name}...]")

                if hasattr(tools, name):
                    func = getattr(tools, name)
                    sig = inspect.signature(func)
                    filtered_args = {k: v for k, v in args.items() if k in sig.parameters}
                    
                    try:
                        result = func(**filtered_args)
                    except Exception as e:
                        print(f" [System: DATABASE ERROR -> {str(e)}]")
                        result = {"status": "error", "message": str(e)}
                else:
                    result = {"status": "error", "message": "Tool not found"}

                conversation_history.append({
                    "tool_call_id": tool.id,
                    "role": "tool",
                    "name": name,
                    "content": json.dumps(result),
                })
            
            # Loop back so the AI reads the tool result
            continue 

        # CASE 2: Final Response
        elif has_content:
            clean_content = msg.content.replace("### Assistant:", "").replace("Assistant:", "").strip()
            conversation_history.append(msg)
            
            # Instead of printing, we return the JSON response to the browser
            return jsonify({"response": clean_content})
        
        else:
            return jsonify({"response": "I'm sorry, I encountered an error processing that."})

if __name__ == "__main__":
    # Ensure you have a 'templates' folder with index.html inside
    app.run(debug=True, port=5000)