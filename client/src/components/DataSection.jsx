import CampaignIcon from "@mui/icons-material/Campaign";
import { Paper } from "@mui/material";
import Title from "./Title";
import CategoryIcon from "@mui/icons-material/Category";
const DataSection = () => {
  return (
    <Paper className="w-3/12 mt-2 p-2 ">
      <Title text={"Data"}></Title>
      <div className="flex justify-between pr-2">
        <div className=" text-primary">
          <CampaignIcon color="#247881" fontSize="large" /> <b>50000+</b>
          <div className="text-black">Tweets analysed</div>
        </div>
        <div className=" text-primary">
          <CategoryIcon color="#247881" fontSize="large" /> <b>9</b>
          <div className="text-black">Topics</div>
        </div>
      </div>
    </Paper>
  );
};

export default DataSection;
