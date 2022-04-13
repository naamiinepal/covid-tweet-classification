import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Samip from "../images/4.jpg";
import GitHubIcon from "@mui/icons-material/GitHub";
import { IconButton } from "@mui/material";
export default function Team() {
  return (
    <div>
      <Typography variant="h3">Our Team</Typography>
      <Card sx={{ maxWidth: 200 }}>
        <CardMedia
          component="img"
          sx={{
            width: 100,
            borderRadius: "50%",
            marginRight: "auto",
            marginLeft: "auto",
            marginTop: "2%",
          }}
          image={Samip}
          alt="Samip"
        />
        <CardContent>
          <Typography
            gutterBottom
            variant="h5"
            component="div"
            className="text-primary"
          >
            Samip Poudel
          </Typography>
        </CardContent>
        <CardActions>
          <IconButton size="small">
            <GitHubIcon />
          </IconButton>
        </CardActions>
      </Card>
    </div>
  );
}
