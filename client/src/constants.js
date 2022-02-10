const baseAddress = "http://localhost:8000";
const columns = [
   
    {
        field: "text",
        label: "Text",
        headerName: "text",
    },
    {
        field: "covid_stats",
        label: "Covid Stats",
        borderColor: "#390ba4",
        backgroundColor: "#390ba4",
        headerName: "covid \n stats",
    },
    {
        field: "vaccination",
        label: "Vaccination",
        borderColor: "#8c0096",
        backgroundColor: "#8c0096",
        headerName: "vaccination",
    },
    {
        field: "covid_politics",
        label: "Covid Politics",
        borderColor: "#bf0082",
        backgroundColor: "#bf0082",
        headerName: "covid \n politics",
    },
    {
        field: "humour",
        label: "Humour",
        borderColor: "#e2006a",
        backgroundColor: "#e2006a",
        headerName: "humour",
    },
    {
        field: "lockdown",
        label: "Lockdown",
        borderColor: "#f90151",
        backgroundColor: "#f90151",
        headerName: "lockdown",
    },
    {
        field: "civic_views",
        label: "Civic Views",
        borderColor: "#ff5039",
        backgroundColor: "#ff5039",
        headerName: "civic \n views",
    },
    {
        field: "life_during_pandemic",
        label: "Life During Pandemic",
        borderColor: "#ff7e1f",
        backgroundColor: "#ff7e1f",
        headerName: "Life During \nPandemic",
    },
    {
        field: "covid_waves_and_variants",
        borderColor: "#ffa600",
        backgroundColor: "#ffa600",
        label: "Covid Waves and Variants",
        headerName: "Covid Waves \n and \n Variants",
    },
     {field: "verify", label: "Verify", headerName: "Verify"},
];
export {baseAddress, columns};
