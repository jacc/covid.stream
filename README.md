
<center>
<br>
  

  <p align="center">
      <img src="https://img.shields.io/badge/dynamic/json?color=informational&label=Live%20version%20Last%20Updated&query=%24.lastUpdated&url=https%3A%2F%2Fapi.covid.stream%2Fstatus%3FgithubPage%3Dtrue"></img>
      <img src="https://img.shields.io/badge/dynamic/json?color=blue&label=Status&query=%24.status&url=https%3A%2F%2Fapi.covid.stream%2Fstatus%3FgithubPage%3Dtrue"></img>
  </p>
  
  <br>
  <h1 align="center">covid.stream</h1>
  <h3 align="center">An API for viewing latest Coronavirus (COVID-19) statistics.</h3>
  <i>
  	Data provided by Johns Hopkins University. This API provided to the public strictly for educational and academic research purposes.
  </i>
</center>

---

## Live version



Endpoint: https://api.covid.stream

### ``/latest/cases`` (GET)

```json
{
    "data": [
        {
            "Province/State": "Hubei",
            "Country/Region": "China",
            "Last Update": "2020-03-12T09:53:06",
            "Confirmed": "67781",
            "Deaths": "3056",
            "Recovered": "50318",
            "Latitude": "30.9756",
            "Longitude": "112.2707"
        }
     ],
    "meta-data": {
        "countriesInfected": [
            "China",
            "Italy",
            "Iran"
        ]
    },
    "apiInformation": {
        "lastUpdated": "03-14-2020"
    }

```

** This endpoint contains **ALL** cases found.**

### ``/latest/cases?filterByCountry=X`` (GET)

Returns the same information but filtered with the country. You can check all countries available by checking the `countriesInfected` key above.

### ``/latest/numbers`` (GET)

```json
{
  "data": {
    "totalConfirmedNumbers": 128343,
    "totalDeathNumbers": 4720,
    "totalRecoveredNumbers": 68324
  }
}
```

**Filter coming soon.**

---

## Disclaimers

Data might not be 100% in line with the version on Jhopkins dasbhoard. Sometimes data can be updated much later. The live version updates every 3 hours.

---

## Rate Limits

No rate limits exist for now, but please remember that data will only be updated every three hours.

---

# Development

---

- No tests at this time.

- PRs are welcome, but Black formatting **is required**,
