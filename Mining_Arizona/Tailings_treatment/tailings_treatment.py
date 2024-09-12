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
def process_tailings_form(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)

            # Extract the form data
            mineral_content = data.get("mineralContent")
            chemical_composition = data.get("chemicalComposition")
            physical_characteristics = data.get("physicalCharacteristics")
            ph_level = data.get("phLevel")
            dissolved_solids = data.get("dissolvedSolids")
            heavy_metals = data.get("heavyMetals")
            quantity = data.get("quantity")
            storage_method = data.get("storageMethod")
            dust_emissions = data.get("dustEmissions")
            treatment_objectives = data.get("treatmentObjectives", [])
            technologies = data.get("technologies", [])
            location = data.get("location")

            # Debug: Print the received data for verification
            print("Received form data:", data)

            # Create a prompt based on the form input
            prompt = f"""
            We are analyzing the following mining tailings:
            - Mineral content: {mineral_content}
            - Chemical composition: {chemical_composition}
            - Physical characteristics: {physical_characteristics}
            - pH level: {ph_level}
            - Dissolved solids: {dissolved_solids}
            - Heavy metals: {heavy_metals}
            - Quantity: {quantity}
            - Storage method: {storage_method}
            - Dust emissions: {dust_emissions}
            - Treatment objectives: {", ".join(treatment_objectives)}
            - Available technologies: {", ".join(technologies)}
            - Location: {location}

            Based on this information and considering the location-specific regulations and environmental conditions, please provide:

            **Procedure:**
            A detailed, step-by-step procedure to effectively treat the tailings, including:
            1. **Duration**: Estimated time required for each step of the process.
            2. **Budget**: Estimated cost for each stage of the treatment, including labor, materials, and equipment.
            3. **Treatment objectives**: Specific types and quantities of neutralizing agents required.
            4. **Available Technologies**: Types and specifications of filtration systems to be used .
            5. **Plan**: A comprehensive treatment plan including any pre-treatment, main treatment steps, and post-treatment processes.

            **Safety Protocols:**
            Safety protocols specifically tailored to the procedure outlined above, including:
            1. **Personal Protective Equipment (PPE)**: Details on the type and specifications of PPE required.
            2. **Chemical Handling**: Guidelines for handling and storage of chemicals used in the treatment.
            3. **Dust Control**: Specific methods and equipment for controlling dust emissions.
            4. **Spill Response**: Detailed procedures and materials for managing spills.
            5. **Monitoring and Sampling**: Frequency and methods for monitoring the treatment process and sampling.

            **Laws & Regulations:**
            Applicable laws and regulations for tailings treatment in the specified location, considering:
            1. **Federal Regulations**: Relevant federal guidelines and compliance requirements.
            2. **State Regulations**: Specific state regulations applicable to the location.
            3. **Local Regulations**: Any additional local ordinances or requirements that must be followed.

            Please ensure that the procedure is accurate and tailored to the provided data, that the safety protocols are aligned with the procedure, and that the laws and regulations are relevant to both the location and the treatment process.
            """
            # Send the prompt to the LLM API using NVIDIA's OpenAI client
            completion = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",  # Ensure the correct model is being used
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
            )

            # Debug: Print the completion object to inspect the structure
            print("Completion response:", completion)

            # Extract the generated content from the API response
            if completion.choices and len(completion.choices) > 0:
                generated_text = completion.choices[0].message.content
            else:
                generated_text = "No response generated."

            # Return the generated response in a JSON response
            return JsonResponse({"success": True, "response": generated_text})

        except Exception as e:
            # Log the exception for debugging
            logger.error(f"Exception occurred: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)