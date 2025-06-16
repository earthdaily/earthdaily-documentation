---
title: Historical Assessment API
description: The Historical Assessment API empowers insurance professionals to request and retrieve historical performance analytics for growers during the policy underwriting phase, enabling objective risk evaluations and faster decisions.
icon: material/api
status: new
---
# Historical Assessment API

The Historical Assessment API empowers insurance professionals to request and retrieve historical performance analytics for growers during the policy underwriting phase, enabling objective risk evaluations and faster decisions.

---

## 🎯 What Is the Historical Assessment API?

The goal of this Historical Assessment API is to equip underwriters from fintech companies with tools to better evaluate the historical performance of growers over the past 5 years (e.g., yield and production variability), enabling a deeper understanding of the risks associated with insuring them.
offers access to five years of agronomic history of an assessed proposal and it(s) field(s), including crop failures, yield variability, and production risk scores.

It is designed for:
- Fintech underwriters
- Risk analysts
- Insurance platform integrators

---

## 🌾 Analytics glossary and definition
The table below describes the analytics used in the Historical Assessment API

| METRIC |DEFINITION| COMMENT |
|--------|----------------|----------------|
| **Historical Potential Score** | NDVI-based score to identify the potential of a given field over the past years. The higher the  value, the better it has performed | Categorization : Very Low (0–40), Low (40–60), Medium (60–70), High (>70)
| **Risk Score** |NDVI-based score leveraging the average potential score to assess the risk/ variability of a field |  Categorization : Low (0–20), Medium (20–30), High (30–60), Very High (>60) 
| **Crop Failure** |  It indicates whether or not the year considered had a normal season or not (NDVI high enough indicating the crop did grow normally or not). |
| **First-Year Cropping** | Based on planting patterns over 5 years, helps the user understand if the insured grower has already had some successful crops on the past years on a given field|

---
## Historical Assessment endpoints summary

*N.B. : This section summarizes the three main endpoints needed to use the Historical Assessment API. Details on the input/output and the various business rules will be found at the **Historical Assessment documentation** section*

Method | Route | Description | Request |
-------|----------------------------------------------|-------------|----------|
|POST      | /fintech/v1/historical-assessment/plots | Ask for a historical assessment for fields within a new policy/proposal |JSON body with list of parameters| 
|POST      | /fintech/v1/historical-assessment/{policyId}   | Perform a historical assessment on a policy / proposal that has already been created.  |endpoint URL with policy ID| 
|GET       |  /fintech/v1/historical-assessment/result/{executionId} | Retrieves the results ot he historical assessment query (once computed)| endpoint URL with historical assessment workflow ID

## 🚀 Historical Assessment documentation

### 🔐 Authentication

All endpoints require secure access via **Identity Server API**, which manages:

- User and application-level authentication  
- Token-based access (OAuth 2.0)  
- Permission scopes to control access to specific data layers or regions

<swagger-ui src="https://api.geosys-na.net/fintech/v1/swagger/v1.0/swagger.json"/>

### 1. Submit a New Proposal
**POST** `/historical-assessment/plots`

Use when declaring a new proposal for the first time. Includes grower details, proposal ID, and field list.

**Request Body**

```json
{
  "user": {
    "login": "string",
    "firstName": "string",
    "lastName": "string",
    "companyName": "string",
    "cpf_Cnpj": "string"
  },
  "proposalNumber": "string",
  "proposalDate": "2025-03-21T16:20:24.978Z",
  "policyNumber": "string",
  "policyDate": "2025-03-21T16:20:24.978Z",
  "insuredFields": [
    {
      "name": "string",
      "geometry": "string",
      "sowingDate": "2025-03-17T10:05:12.053Z",
      "crop": {
        "id": "string"
      }
    }
  ]
}
;
```


* **user**: - Object containing user information
  * **login**: User's login.
      * If the user login is known, the policies and its field will be created within the existing grower, and only the login is mandatory. If not, the API endpoint also needs either the firstname and lastname, or the companyName.
  * **firstName**: User's first name.
    * Mandatory if LastName is used
  * **lastName**: User's last name.
    * Mandatory if FirstName is used
  * **companyName**: Name of the user's associated company.
  * **cpf_cnpj**: CPF or CNPJ number (Cadastro de Pessoas Físicas)
* **proposalNumber**: Identifier of the insurance proposal. Can be null if policyNumber is not null.
* **proposalDate**: Creation date of the insurance proposal. Default, current date when object is created.
* **policyNumber**: Identifier of the insurance policy. Can be null if proposalNumber is not null.
* **policyDate**: Creation date of the insurance policy.
* **insuredFields**: Array of objects representing insured fields for which the user wants to perform a historical assessment.
  * **name**: Name of the insured field.
  * **geometry** : [MANDATORY] - Geometry of the field's boundaries in WKT
  * **sowingDate** [MANDATORY] - Date when the crop was sown (YYYY-MM-DD)
  * **crop**: [MANDATORY] Object containing crop details.
    * **id**: Unique crop identifier. Ex : CORN, SOYBEANS, 2ND_CORN…

**Response body**

```json
{
  "executionId": "string"
}
```
<br>

An `executionId` to track progress of the workflow computing the historical assessment analytics and retrieve results with the **GET** `/historical-assessment/result/{executionId}`

N.B. : if performed on an already existing policy or proposal, this endpoint will return an error, suggesting the user to query the historical assessment through the following endpoint instead.

### 2. Submit an Existing Proposal

**POST** `/historical-assessment/{policyId}`

Use this endpoint if the proposal already exists in the system.

**Step 1:** Retrieve technical `policyId` using:

**GET** `/policies?proposalNumber=X`

**Step 2:** Submit that `policyId` to the historical assessment endpoint above

**Response body**

```json
{
  "executionId": "string"
}
```

An `executionId` to track progress of the workflow computing the historical assessment analytics and retrieve results with the **GET** `/historical-assessment/result/{executionId}`

N.B. : if performed on an already existing policy or proposal, this endpoint will return an error, suggesting the user to query the historical assessment through the following endpoint instead.

### 3. Retrieve Results

**GET** `/historical-assessment/result/{executionId}`

Returns full results:
- Assessment computation status: `RUNNING`, `FAILED`, `SUCCEEDED`
- Proposal metadata
- Summary indicators
- Field-level breakdowns

Response body example
```json
{
    "assessmentStatus": "SUCCEEDED",
    "assessmentResults": {
        "proposalNumber": "17282892211",
        "proposalDate": "2025-03-19",
        "policyNumber": "string",
        "policyDate": "2025-03-21",
        "totalAcreage": 280.1,
        "firstYearCroping": "FALSE",
        "cropFailure": true,
        "averageRiskScore": 27.6,
        "riskScoreCategory": "MEDIUM",
        "averagePotentialScore": 86.7,
        "potentialScoreCategory": "HIGH",
        "plots": [
            {
                "id": "52G0PSktQjsHGzbFnUbypJ",
                "fieldName": "1",
                "acreage": 125,
                "firstYearCroping": "FALSE",
                "cropFailure": true,
                "averageRiskScore": 22.6,
                "resultsBySeason": {
                    "2024": {
                        "potentialScore": 56.6,
                        "cropFailure": true,
                        "plantedStatus": true
                    },
                    "2023": {
                        "potentialScore": 98.2,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2022": {
                        "potentialScore": 88.2,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2021": {
                        "potentialScore": 110.2,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2020": {
                        "potentialScore": 87.5,
                        "cropFailure": false,
                        "plantedStatus": true
                    }
                }
            },
            {
                "id": "4rprGh0Mmjop6zPG8OF6aY",
                "fieldName": "2",
                "acreage": 155.1,
                "firstYearCroping": "FALSE",
                "cropFailure": true,
                "averageRiskScore": 31.7,
                "resultsBySeason": {
                    "2024": {
                        "potentialScore": 48.1,
                        "cropFailure": true,
                        "plantedStatus": true
                    },
                    "2023": {
                        "potentialScore": 67.9,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2022": {
                        "potentialScore": 102.4,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2021": {
                        "potentialScore": 114.7,
                        "cropFailure": false,
                        "plantedStatus": true
                    },
                    "2020": {
                        "potentialScore": 94.8,
                        "cropFailure": false,
                        "plantedStatus": true
                    }
                }
            }
        ]
    }
}
```

- **Root Level**
  - **assessmentStatus**: string indicating the status of the assessment. Possible values:
    - **RUNNING**: the historical assessment workflow is still computing the analysis, `assessmentResults` are not available yet.
    - **FAILED**: a technical problem has occurred (details will be given to the user in the `errors` attribute).
    - **SUCCEEDED**: the workflow is done and the results are available.
  - **errors**: only when errors are encountered. Displays detailed messages on the error(s) encountered.

- **assessmentResults Object**
  - **proposalNumber**: string with the proposal identifier.
  - **proposalDate**: string with the proposal date (format: YYYY-MM-DD).
  - **policyNumber**: string with the policy identifier.
  - **policyDate**: string with the policy date (format: YYYY-MM-DD).
  - **totalAcreage**: number representing the total acreage assessed.
  - **firstYearCroping**: enumeration indicating if it's the first year of cropping
    - **TRUE**: if there is at least one plot with status = true.
    - **TO BE ANALYZED**: if there is at least one plot with status = to be analyzed (and no plot having the TRUE status).
    - **FALSE**: if all plots are false (meaning that they all have cropping history)
  - **cropFailure**: boolean indicating if there was a crop failure on the proposal (taking into account the last 5 years)
    - `true`: if at least one plot within the proposal experienced a crop failure.
    - `false`: otherwise.
  - **averageRiskScore**: number representing the average risk score across all plots on the last 5 years, weighted by area and computed on the season of interest.
  - **riskScoreCategory**: string categorizing the risk score
    - Low (0-20)
    - Medium (20-30)
    - High (30-60)
    - Very High (>60)
  - **averagePotentialScore**: number representing the average potential score.
  - **potentialScoreCategory**: string categorizing the potential score
    - Very Low (0-40)
    - Low (40-60)
    - Medium (60-70)
    - High (>70)

- **Each Plot Object (within `plots` array)**
  - **id**: string representing the unique plot ID.
  - **fieldName**: string identifying the plot name or number.
  - **acreage**: number representing the size of the plot.
  - **firstYearCroping**: enumeration for the plot’s first cropping year status
    - The last two years are planted → **FALSE**
    - Over the last 2 years, there are 0 or 1 planted year:
      - Over the last 5 years, at least 3 were planted → **TO BE ANALYZED**
      - Over the last 5 years, fewer than 3 were planted → **TRUE**
  - **cropFailure**: boolean indicating if there was a crop failure on the plot (taking into account the last 5 years)
    - `true`: if at least one year within the plot experienced a crop failure.
    - `false`: otherwise.
  - **averageRiskScore**: number showing the average risk score for the plot (taking into account the last 5 years).
  - **resultsBySeason Object**: object grouping historical data by year (per plot)
    - **Keys**: years as strings (e.g., "2024", "2023", etc.), starting from the current year minus one.
    - Each year contains:
      - **potentialScore**: number representing the potential score for that year.
      - **cropFailure**: boolean indicating if there was a crop failure that year.
      - **plantedStatus**: boolean showing if planting occurred that year.


## 📚 Developer Resources

- [Swagger UI – Production](https://api.geosys-na.net/fintech/v1/swagger/index.html)

---

Need Postman collections or API keys? Reach out to your EarthDaily Agro contact.
