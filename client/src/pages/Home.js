import React from "react";
import { Container, Header, Segment } from "semantic-ui-react";
import '../stylesheets/Home.css'

export default function Home() {
  return (
    <Container>
      <div className="home-header_wrapper">
        <Header className="home-header">Welcome to the <b>F&L Launch Planning Tool</b>!</Header>
        <p className="home-header">This tool is meant for pre-launch planning activities in order for planners, launch managers, and F&L partners to work effectively in generating different ship and build plans for future launches. Please follow the steps outlined below.</p>
      </div>
      <Segment>
        <p><b>1.</b> Please start by navigating to <b>Launch Profiles</b> and creating a launch profile via the web or the excel upload functionality.</p>
        <p><b>2.</b> After creaing a launch profile you create a <b>Launch Plan</b> in the "Launch Plans" section by downloading, filling out and uploading the provided excel template. When uploading your launch plans you will associate that plan file to your created <b>launch profile</b>.</p>
        <p><b>3.</b> Once a launch plan is created the tool will automatically create a ship and build plan based on the data entered for download and viewership found in the <b>Launch Insights</b> section.</p>
        <p><b>4.</b> As users create launch profiles and launch plans users will be able to <b>download and re-upload previously entered profiles and plans to edit</b> changing the meta data of a profile and or run different plan scenarios. Each new or changed launch plan will be assigned a version number as well as associated derived ship and build plans.</p>
      </Segment>
    </Container>
  );
}