import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from openai import OpenAI  # Ensure correct OpenAI client for NVIDIA Llama-3
import json
import os
from cryptography.fernet import Fernet


'''encryption_key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(encryption_key.encode())
encrypted_key = os.getenv('ENCRYPTED_API_KEY')
decrypted_api_key = cipher_suite.decrypt(encrypted_key.encode()).decode()'''
decrypted_api_key = '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'

logger = logging.getLogger(__name__)

# Initialize the OpenAI client for NVIDIA Llama-3
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=decrypted_api_key
)

@csrf_exempt
def comment_analysis(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)

            # Extract the form data
            comment_text = data.get('comment')

            # Debug: Print the received data for verification
            print("Received form data:", data)

            # Create a prompt based on the form input
            prompt = f"""
            We are analyzing the risk of given comment:
            - comment: {comment_text}

            Based on this information provide risk_analysis as high or moderate or low:
            ** put ////t infront of risk_factor and back ////t
            ** sample risk_factor:////t<riak_analysis> ////t it makes easier to extract data.
            """
            # Send the prompt to the LLM API using NVIDIA's OpenAI client
            risk_analysis = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",  # Ensure the correct model is being used
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
            )

            # Debug: Print the completion object to inspect the structure
            print("Completion response:", risk_analysis)

            # Extract the generated content from the API response
            data = {}
            if risk_analysis.choices and len(risk_analysis.choices) > 0:
                generated_text = risk_analysis.choices[0].message.content
                data_division = generated_text.split("////t")
                data = {
                    "success": True,
                    "response":{
                        "risk_factor": data_division[1],
                        "comment": comment_text
                    }
                }
                print(data.get("response").get("risk_factor"))
                print(data.get("response").get("comment"))
            else:
                generated_text = "No response generated."
                data = {
                    "Error": generated_text
                }

            # Return the generated response in a JSON response
            return JsonResponse({"success": True, "response": data})

        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Exception occurred: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)