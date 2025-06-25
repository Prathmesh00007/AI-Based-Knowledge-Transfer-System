// src/App.jsx
import React from "react";
import Auth from "./components/Auth";
import JiraConnector from "./components/JiraConnector";
import ConfluenceIngest from "./components/ConfluenceConnector";
import Search from "./components/Search";
import Record from "./components/Record";
import PipelineTest from "./components/Pipeline";

const App = () => {
  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Knowledge Transfer System</h1>
      <Auth />
      <JiraConnector />
      <ConfluenceIngest />
      <Search />
      <Record />
      <PipelineTest />
    </div>
  );
};

export default App;
