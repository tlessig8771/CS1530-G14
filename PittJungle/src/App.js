import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div></div>
      <img src={require ('./logo.png')}></img>
      <h1 className = "title">PittJungle!</h1>
     
    {/*} <button onclick = {() => href = "https://stackoverflow.com/questions/30766441/reactjs-how-to-use-comments"}>LogIn</button>*/}
     <a href="https://stackoverflow.com/questions/30766441/reactjs-how-to-use-comments">LogIn</a>
      <header className="App-header">
    

        <h1>Welcome to PittJungle!</h1>
        <h2 className="subheading">The Issue: </h2>
        <p>When students are starting college, it is the first time they are on their own. Students tend to focus their time on academics, which although is important, can be detrimental to their overall college experience. We hope our product can bridge the gap between academics and leisure by introducing students to dining options other than university dining halls, as well as other local events and attractions. </p>
        <h2 className="subheading">Our Mission: </h2>
        <p>Our team will put together a product called PittJungle. It will mainly be used as a navigation tool for Pitt students to find local events, eateries, academic recommendations and activities on and around campus. It will allow students to create groups and communities with people who have similar interests. This will help new students create a life outside of class which is vital for a college lifestyle. </p>

        <h2 className="subheading">The Team: </h2> 
        <p>Sush, Sherryl, Trent, Luiza and David</p>
        
      </header>
    </div>
  );
}

export default App;
