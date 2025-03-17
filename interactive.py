
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("Professional Style Learning System")
    print("=================================")
    
    # Get profession
    profession = input("What is your profession? (e.g., doctor, therapist, realtor): ")
    
    # Sample questions for different professions
    questions = {
        "doctor": [
            "A patient messages you saying they have a mild fever and body aches for 2 days. How would you respond?",
            "A patient asks if they should be worried about a new medication's side effects. How would you respond?",
            "Someone wants to know if their lab results are concerning. How would you respond?",
            "A patient asks you to explain a common procedure in your field. How would you respond?",
            "Someone asks for your opinion on a popular health trend. How would you respond?"
        ],
        "therapist": [
            "A client messages you saying they're feeling anxious about a job interview. How would you respond?",
            "Someone tells you they've been feeling unmotivated lately. How would you respond?",
            "A client asks how they can improve their relationship with their partner. How would you respond?",
            "Someone wants to know if their feelings of sadness are normal. How would you respond?",
            "A client asks how many sessions they might need. How would you respond?"
        ],
        "realtor": [
            "A potential buyer asks when they can see a property you've listed. How would you respond?",
            "Someone asks if now is a good time to sell their home. How would you respond?",
            "A client asks what they should do to prepare their house for showing. How would you respond?",
            "Someone asks about property values in a specific neighborhood. How would you respond?",
            "A potential client asks why they should work with you instead of another agent. How would you respond?"
        ]
    }
    
    # Use default questions if profession not found
    default_questions = [
        "A client asks when they can schedule an appointment with you. How would you respond?",
        "Someone asks about your rates or fees. How would you respond?",
        "A client wants to know your professional opinion on something. How would you respond?",
        "Someone requests more information about your services. How would you respond?",
        "A potential client asks why they should work with you. How would you respond?"
    ]
    
    # Get the appropriate questions for the profession
    prof_questions = questions.get(profession.lower(), default_questions)
    
    # Collect responses
    responses = []
    print("\nWe'll now ask you 5 questions to learn your communication style.")
    print("Please respond as you naturally would in a professional context.\n")
    
    for i, question in enumerate(prof_questions):
        print(f"Question {i+1}:")
        print(question)
        response = input("Your response: ")
        responses.append(response)
        print()
    
    # Analyze style
    print("Analyzing your communication style...")
    style_analysis = analyze_style(responses, profession)
    print("\nStyle Analysis:")
    print(style_analysis)
    
    # Test with custom questions
    while True:
        print("\nTest if the system has learned your style.")
        print("Enter a question that a client might ask you (or type 'exit' to quit):")
        test_question = input("> ")
        
        if test_question.lower() == 'exit':
            break
            
        styled_response = generate_styled_response(test_question, {
            "profession": profession,
            "responses": responses,
            "style_analysis": style_analysis
        })
        
        print("\nGenerated response in your style:")
        print(styled_response)
        
        feedback = input("\nDoes this sound like your style? (yes/no): ")
        if feedback.lower() == 'no':
            print("Thank you for the feedback. This helps improve the system.")

def analyze_style(responses, profession):
    """Analyze the user's response style"""
    prompt = f"""
    Analyze the communication style in these responses from a {profession}. 
    Identify patterns in tone, sentence structure, vocabulary, and any distinctive elements.
    
    Responses:
    1. {responses[0]}
    2. {responses[1]}
    3. {responses[2]}
    4. {responses[3]}
    5. {responses[4]}
    
    Provide a detailed style analysis that can be used to mimic this person's communication style.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a communication style analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def generate_styled_response(question, user_profile):
    """Generate a response in the user's style"""
    examples = "\n".join([f"{i+1}. {resp}" for i, resp in enumerate(user_profile['responses'])])
    
    prompt = f"""
    You are a {user_profile['profession']} with the following communication style:
    
    {user_profile['style_analysis']}
    
    Here are some examples of how you respond to questions:
    {examples}
    
    Please respond to this question in your typical communication style:
    "{question}"
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are mimicking a specific professional's communication style."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    main()