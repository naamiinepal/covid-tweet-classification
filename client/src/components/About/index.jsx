import Nav from "../Nav";
import Title from "../Title";
import Teams from "./Teams";

const About = () => {
  return (
    <div>
      <Nav />
      <div className="ml-16 mt-3 w-11/12 text-center">
        <Title text="Abstract" />
        <div className="text-justify mt-3">
          The escalation in social media usage amid the pandemic has gathered
          extensive data for Natural Language Processing tasks, many of which
          solve some of the contemporary issues of the world. An abundance of
          these NLP tasks focuses on widely spoken languages like English.
          Moreover, researchers haven’t exploited the true potential of NLP and
          the available data to extract a solution for prominent issues like the
          COVID-19 epidemic. We, through this project, present a COVID tweets
          analysis platform that allows health decision-makers to view a
          real-time analysis of narratives of tweets, particularly in Nepali and
          Devanagari scripts. Our method enables stakeholders to look into the
          public conversation and trends surrounding the COVID-19 epidemic. We
          categorize the tweets across nine curated (mapped from WHO) topics
          using a MuRIL model to summarize our insights. Experimental results
          reveal the essence of our model as it can classify the tweets with
          appropriate scores for the evaluation metrics. The analysis of the
          results shows that our model can portray the growth in the discussions
          relating to different phases of the epidemic.
        </div>
        <Teams />
      </div>
    </div>
  );
};

export default About;
