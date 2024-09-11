import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from openai import OpenAI  # Ensure correct OpenAI client for NVIDIA Llama-3
import json

logger = logging.getLogger(__name__)

# Initialize the OpenAI client for NVIDIA Llama-3
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
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
            Based on this information, provide a step-by-step procedure to treat the tailings.
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
