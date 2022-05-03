import { Paper } from "@mui/material";
import Title from "./Title";
import DataSection from "./DataSection";
import Nepal from "../svgs/nepal.svg"
const Purpose = () => (
  <div className="ml-16 w-11/12 flex justify-between">
  <Paper className="w-3/12 mt-2 p-2">
    <Title text={"An Idea Behind"}></Title>
    Listening to people's questions and concerns is an important way for health
    authorities to learn about what matters to communities in response to
    COVID-19.
  </Paper>
  <img alt="NAAMII-Logo" src={Nepal} width="100" />

  <DataSection/>
  </div>
);

export default Purpose;
