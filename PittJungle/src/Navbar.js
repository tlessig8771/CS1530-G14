import React, { Component } from 'react';
import { Button } from "./Button"
import logo from "./logo.png"
import './Navbar.css'
import './Food.js'
import './App.js'
import './Attractions.js'
import './HomePage.js'
import {Link} from 'react-router-dom';



class Navbar extends Component {
    state = { clicked: false }

    handleClick = () => {
        this.setState({ clicked: !this.state.clicked })
    }

    render() {
        return(
            <div>

            <nav className="NavbarItems">
               <Link to = "/"><img src={logo} height = "50" width = "55"/></Link>
                <h1 className="navbar-logo"><Link to = "/"style={{ textDecoration: 'none', color: "white"}} >PittJungle</Link><i className="fab fa-react"></i></h1>
                <div className="menu-icon" onClick={this.handleClick}>
                    <i className={this.state.clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
                </div>
                <ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}>
                    <Link to="/Food" style={{ textDecoration: 'none'}}><Button>Food</Button></Link>
                    <Link to="/Attractions" style={{ textDecoration: 'none'}} ><Button>Attractions</Button></Link>
                    <Link to="" style={{ textDecoration: 'none'}} ><Button>Events</Button></Link>
                    <Link to="" style={{ textDecoration: 'none'}} ><Button>How-To</Button></Link>
                </ul>
                <Button>Sign Up</Button>
            </nav>
            </div>
        )
    }
}

export default Navbar