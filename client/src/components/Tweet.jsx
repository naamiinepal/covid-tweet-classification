import { Button, Card, Chip } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { months } from "../constants";
const Tweet = ({ tweet }) => {
  const created_date = new Date(tweet.created_at);
  return (
    <Card className="p-5 mb-2" variant="outlined">
      <div>
        <PersonIcon />
        <span className="text-primary"> {tweet.username}</span> on{" "}
        <span className="text-primary">
          {months[created_date.getMonth()]} {created_date.getDate()},{" "}
          {created_date.getFullYear()}
        </span>
      </div>
      {tweet.text}
      <div className="mt-1 flex">
        {tweet &&
          Object.keys(tweet)
            .filter(
              (col) =>
                col !== "id" &&
                col !== "created_at" &&
                col !== "text" &&
                col !== "username"
            )
            .map((rowElement) => {
              if (tweet[rowElement]) {
                return (
                  <Chip className="mr-1" label={rowElement} color="success" />
                );
              } else {
                return <></>;
              }
            })}
        <Button sx={{ marginLeft: "auto" }}>{"Edit"}</Button>
      </div>
    </Card>
  );
};

export default Tweet;
