# EUDAMED HELPER

AI workflow to for gaining insights into the eudamed database


## Workflow

1. User input
2. AI agent (ask followup questions)
    - There should be some criteria that the agent is trying to reach before being satisfied with questions
3. Agent fetch data via EUDAMED api
4. (Optional) Use RAG db from legal documentations for information retrieval if necessary
5. Return back answer to user with references to legal documentation.


## Prerequisites: 
- If you dont have .zshrc file, then create on in your user root folder
- Put ´GEMINI_API_KEY´as variable in .zshrc file
- Restart terminal och or source the .zshrc file 
ALSO:
- if you dont have python on your computer, then install python3.12 (is best i think)
    - i like to use homebrew(brew), google how to install brew.
    - then install python3.12 via brew (google this also)

## HOW TO RUN THE PROGRAM
Open mac terminal and type:
1. ```make activate```
2. ```make run```


## Other information
Good api that we could use for thesis case
https://github.com/openregulatory/eudamed-api

The records in EUDAMED includes these fields:
"basicUdi" : "XXXXXXXXXXXXX",
"primaryDi" : "XXXXXXXXXXXXX",

Since similar records from the same company have different basicUdi and different primaryDi it is more interesting to filter searches so that we dont have collections that share the same basicUdi.


## The rules graph

::: mermaid
graph TD
    %% Start och Initial Analys
    Start((Start)) --> Triage["<b>Triage Node</b><br/>Analysera input<br/>Sätt flaggor: is_active, invasive_type"]
    
    Triage --> CheckActive{"<b>Är den Active?</b><br/>(Conditional Edge)"}

    %% Active Branch (Rule 9-13)
    CheckActive -- Ja --> AskActive["<b>Active Questions Node</b><br/>Fråga om energi, mjukvara,<br/>vital monitoring (Rule 9-13)"]
    CheckActive -- Nej --> CheckInvasive

    %% Koppla Active vidare till Physical (Vattenfall)
    AskActive --> CheckInvasive{"<b>Vilken Invasiv typ?</b><br/>(Conditional Edge)"}

    %% Physical Branches (Rule 1-8)
    CheckInvasive -- Non-Invasive --> AskNonInv["<b>Non-Invasive Questions Node</b><br/>Fråga om skadad hud,<br/>vätskor etc (Rule 1-4)"]
    CheckInvasive -- Invasive / Implant --> AskInv["<b>Invasive Questions Node</b><br/>Fråga om duration,<br/>centrala organ (Rule 5-8)"]

    %% Samling vid Special Rules (Rule 14-22)
    AskNonInv --> AskSpecial
    AskInv --> AskSpecial

    AskSpecial["<b>Special Rules Node</b><br/>Fråga om nanomaterial,<br/>mediciner etc (Rule 14-22)"]

    %% Final Classification
    AskSpecial --> Classify["<b>Classifier Node</b><br/>Jämför Active Result vs Physical Result<br/>Högsta klassificering vinner"]
    
    Classify --> End((Slut))

    %% Styling
    classDef logic fill:#f9f,stroke:#333,stroke-width:2px;
    classDef question fill:#bbf,stroke:#333,stroke-width:2px;
    classDef result fill:#bfb,stroke:#333,stroke-width:2px;

    class CheckActive,CheckInvasive logic;
    class AskActive,AskNonInv,AskInv,AskSpecial question;
    class Classify result;
:::