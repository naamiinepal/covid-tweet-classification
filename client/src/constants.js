const baseAddress = "http://localhost:8000";
const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];
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
        description:
            " Statistics about new cases, deaths, total cases, tests, casualties, etc.",
    },
    {
        field: "vaccination",
        label: "Vaccination",
        borderColor: "#8c0096",
        backgroundColor: "#d58c32",
        headerName: "vaccination",
        description: "Serious information regarding vaccination.",
    },
    {
        field: "covid_politics",
        label: "Covid Politics",
        borderColor: "#bf0082",
        backgroundColor: "#a4a031",
        headerName: "covid \n politics",
        description:
            "National and International politics closely concerned with Covid.",
    },
    {
        field: "humour",
        label: "Humour",
        borderColor: "#e2006a",
        backgroundColor: "#50b131",
        headerName: "humour",
        description: "Satire, humour related to Covid.",
    },
    {
        field: "lockdown",
        label: "Lockdown",
        borderColor: "#f90151",
        backgroundColor: "#34ae91",
        headerName: "lockdown",
        description:
            "Information regarding lockdown, nisedhagyas, exams during lockdown.",
    },
    {
        field: "civic_views",
        label: "Civic Views",
        borderColor: "#ff5039",
        backgroundColor: "#37abb5",
        headerName: "civic \n views",
        description: "General views, suggestions, rants from the public.",
    },
    {
        field: "life_during_pandemic",
        label: "Life During Pandemic",
        borderColor: "#ff7e1f",
        backgroundColor: "#3ba3ec",
        headerName: "Life During \nPandemic",
        description: "Effect of covid on day-to-day activities of the public.",
    },
    {
        field: "covid_waves_and_variants",
        borderColor: "#ffa600",
        backgroundColor: "#bb83f4",
        label: "Covid Waves and Variants",
        headerName: "Covid Waves \n and \n Variants",
        description: "Different waves and variants of the virus.",
    },
    {
        field: "others",
        borderColor: "#ffa600",
        backgroundColor: "#f564d4",
        label: "Others",
        headerName: "Others",
        description: "Not related to any Covid Categories,",
    },
    {field: "verify", label: "Verify", headerName: "Verify"},
];
export {baseAddress, columns, months};
