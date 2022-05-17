import React from "react";
import Title from "../Title";
import Samip from "../../images/4.jpg";
import Nirajan from "../../images/Nirajan.jpg";
import Rabin from "../../images/Rabin.jpg";
import Safal from "../../images/Safal.png";
import AmanSir from "../../images/AmanSir.jpeg";
import BisheshSir from "../../images/BisheshSir.jpeg";

const Teams = () => {
  return (
    <div className="text-center">
      <Title text="Our Team" />
      <div className="flex justify-around my-6 items-center">
        <div className="text-center">
          <img
            src={Nirajan}
            alt="Nirajan"
            width="100"
            className="rounded-full mx-auto"
          />
          <div>Nirajan Basnet</div>
          <div>IOE, Pulchowk Campus</div>
        </div>
        <div className="text-center">
          <img
            src={Rabin}
            alt="Rabin"
            width="100"
            className="rounded-full mx-auto"
          />
          Rabin Adhikari
          <div>IOE, Pulchowk Campus</div>
        </div>
        <div className="text-center">
          <img
            src={Safal}
            alt="Safal"
            width="100"
            className="rounded-full mx-auto"
          />
          Safal Thapaliya
          <div>IOE, Pulchowk Campus</div>
        </div>
        <div className="text-center">
          <img
            src={Samip}
            alt="Samip"
            width="100"
            className="rounded-full mx-auto"
          />
          Samip Poudel
          <div>IOE, Pulchowk Campus</div>
        </div>
      </div>
      <Title text="Our Supervisors" />
      <div className="flex justify-around  my-6 items-center">
        <div className="text-center">
          <img
            src={AmanSir}
            alt="Aman Sir"
            width="100"
            className="rounded-full mx-auto"
          />
          Dr. Aman Shakya
          <div>Assistant Professor</div>
          <div>IOE, Pulchowk Campus</div>
        </div>
        <div className="text-center">
          <img
            src={BisheshSir}
            alt="BisheshSir"
            width="100"
            className="rounded-full mx-auto"
          />
          Dr. Bishesh Khanal
          <div>Director</div>
          <div>NAAMII</div>
        </div>
      </div>
    </div>
  );
};

export default Teams;
