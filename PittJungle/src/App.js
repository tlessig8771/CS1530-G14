import React from 'react';
// import './App.css';

import HomePage from './HomePage.js';
import Food from './Food.js';
import Attractions from './Attractions.js'
import './Navbar';

import { BrowserRouter, Route, Switch, Link, Redirect } from 'react-router-dom';


function App() {
  return (
     <BrowserRouter>
     <Switch>
        <Route exact path ="/" component = {HomePage}></Route>
        <Route exact path="/Food" component = {Food}></Route>
        <Route exact path="/Attractions" component = {Attractions}></Route>
     </Switch>   
    </BrowserRouter>
  )
}


export default App;
