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
        backgroundColor: "#f77189",
        headerName: "covid \n stats",
    },
    {
        field: "vaccination",
        label: "Vaccination",
        borderColor: "#8c0096",
        backgroundColor: "#d58c32",
        headerName: "vaccination",
    },
    {
        field: "covid_politics",
        label: "Covid Politics",
        borderColor: "#bf0082",
        backgroundColor: "#a4a031",
        headerName: "covid \n politics",
    },
    {
        field: "humour",
        label: "Humour",
        borderColor: "#e2006a",
        backgroundColor: "#50b131",
        headerName: "humour",
    },
    {
        field: "lockdown",
        label: "Lockdown",
        borderColor: "#f90151",
        backgroundColor: "#34ae91",
        headerName: "lockdown",
    },
    {
        field: "civic_views",
        label: "Civic Views",
        borderColor: "#ff5039",
        backgroundColor: "#37abb5",
        headerName: "civic \n views",
    },
    {
        field: "life_during_pandemic",
        label: "Life During Pandemic",
        borderColor: "#ff7e1f",
        backgroundColor: "#3ba3ec",
        headerName: "Life During \nPandemic",
    },
    {
        field: "covid_waves_and_variants",
        borderColor: "#ffa600",
        backgroundColor: "#bb83f4",
        label: "Covid Waves and Variants",
        headerName: "Covid Waves \n and \n Variants",
    },
    {
        field: "others",
        borderColor: "#ffa600",
        backgroundColor: "#f564d4",
        label: "Others",
        headerName: "Others",
   
    },
     {field: "verify", label: "Verify", headerName: "Verify"},
];
export {baseAddress, columns};
