import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_style(responses, profession):
    """
    Analyze a professional's communication style based on their responses
    """
    prompt = f"""
    Analyze the communication style in these responses from a {profession}. 
    Identify patterns in tone, sentence structure, vocabulary, and any distinctive elements.
    
    Responses:
    """
    
    for i, resp in enumerate(responses):
        prompt += f"\n{i+1}. Question: {resp['question']}\n   Response: {resp['response']}\n"
    
    prompt += """
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

def analyze_customer_notes(notes, customer_name):
    """
    Analyze customer notes to identify communication opportunities
    """
    note_text = "\n".join([note["content"] for note in notes])
    
    prompt = f"""
    Analyze these notes about {customer_name} and identify any communication opportunities:
    
    {note_text}
    
    Look for:
    1. Upcoming or recent birthdays or anniversaries
    2. Health concerns that warrant follow-up
    3. Expressed interests that you could comment on (sports, hobbies)
    4. Recent life events (moves, job changes, etc.)
    5. Seasonal opportunities (holidays, weather events)
    
    For each opportunity, provide:
    - The communication trigger
    - Suggested timing (immediate, this week, this month)
    - Recommended medium (SMS or email)
    - The specific detail from notes to reference
    - Importance score (1-10 with 10 being highest)
    
    Return your analysis in JSON format as shown below:
    {{
      "opportunities": [
        {{
          "trigger": "trigger_description",
          "timing": "immediate|this_week|this_month",
          "medium": "sms|email",
          "reference": "specific detail to mention",
          "importance": 1-10
        }}
      ]
    }}
    
    If no good opportunities exist, return an empty opportunities array.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI that identifies optimal client communication opportunities. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
        # Removed the response_format parameter that was causing the error
    )
    
    try:
        # Since we're not using response_format, we need to parse the content as JSON
        content = response.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError:
        # If parsing fails, return a default structure
        print(f"Error parsing JSON from response: {response.choices[0].message.content}")
        return {"opportunities": []}

def generate_styled_message(user_data, customer_data, notes, message_type="sms", reference_detail=None):
    """
    Generate a message in the user's style based on customer notes
    """
    # Extract key information from notes
    note_text = "\n".join([note["content"] for note in notes])
    
    reference_prompt = ""
    if reference_detail:
        reference_prompt = f"\nSpecifically, be sure to reference this detail: {reference_detail}"
    
    prompt = f"""
    You are a {user_data['profession']} with the following communication style:
    
    {user_data['style_analysis']}
    
    You need to write a {message_type} to your client/customer named {customer_data['name']}.
    
    Here are your notes about this customer:
    {note_text}
    {reference_prompt}
    
    Write a personalized {message_type} that incorporates information from your notes.
    Keep it natural, friendly, and authentic to your communication style.
    If it's a birthday message, make it appropriate for the occasion.
    If there are health concerns or specific interests mentioned, reference them appropriately.
    
    The message should be concise (appropriate for {message_type}) and not explicitly mention that you're using notes.
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