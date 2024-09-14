from openai import OpenAI
client = OpenAI(
    api_key="<Replace you'r API key here>",
)

client.images.generate(
  model="dall-e-3",
  prompt="Generate poster of the Procedure: To effectively treat the mining tailings, the following step-by-step procedure is recommended:"
         "1. Pre-treatment preparation (Duration: 2 weeks, Budget: $150,000)"
         "* Clear the area around the tailings storage facility to prevent any obstacles during the treatment process."
         "* Install a drainage system to prevent water accumulation."
         "* Materials Required: Excavators, drainage pipes, and fittings."
         "* Equipment Required: Backhoe loaders, excavators."
         "2. Neutralization (Duration: 4 weeks, Budget: $300,000)"
         "* Apply lime neutralization to raise the pH level and reduce the acidity of the tailings."
         "* Quantity of neutralizing agents required: 500 tons of lime."
         "* Materials Required: Lime, water, and mixing equipment."
         "* Equipment Required: Lime spreaders, mixers, and water tanks."
         "3. Filtration (Duration: 6 weeks, Budget: $400,000)"
         "* Install a membrane filtration system to remove dissolved solids and heavy metals."
         "* Types and specifications of filtration systems: Ultrafiltration (UF) membranes with a pore size of 0.01 microns."
         "* Materials Required: UF membranes, pumps, and piping."
         "* Equpment Required: Filtration units, pumps, and control systems."
         "4. Heavy metal precipitation (Duration: 2 weeks, Budget: $100,000)"
         "* Apply chemical precipitation to remove heavy metals such as lead and cadmium."
         "* Quantity of precipitating agents required: 100 tons of sodium hydroxide."
         "* Materials Required: Sodium hydroxide, mixing equipment, and settling tanks."
         "* Equipment Required: Mixers, pumps, and settling tanks."
         "5. Final disposal (Duration: 2 weeks, Budget: $50,000)"
         "* Dispose of the treated tailings in a designated area."
         "* Materials Required: Trucks, excavators, and compactors."
         "* Equipment Required: Trucks, excavators, and compactors."
         "1. Week 1-2: Pre-treatment preparation"
         "2. Week 3-6: Neutralization"
         "3. Week 7-12: Filtration"
         "4. Week 13-14: Heavy metal precipitation"
         "5. Week 15-16: Final disposal"
         "Enhance the poster to clearly",
  n=1,
  size="1024x1024"
)
