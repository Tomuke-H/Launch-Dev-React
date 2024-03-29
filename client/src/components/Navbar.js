import React, { useContext } from 'react'
import { Link, useHistory, withRouter } from 'react-router-dom'
import { Menu } from 'semantic-ui-react'
import { AuthContext } from '../providers/AuthProvider'


const Navbar = (props) => {
  const { user, handleLogout} = useContext(AuthContext)
  const history = useHistory();
  const { location } = props;

  const rightNavItems = () =>{
    if(user){
      return (
        <Menu.Item onClick={()=> handleLogout(history)}>Logout</Menu.Item>
      ) ;
    };
    return (
      <>
        <Link to='/login'>
          <Menu.Item active={location.pathname === '/login'} >
            Login
          </Menu.Item >
        </Link>
        <Link to='/register'>
          <Menu.Item active={location.pathname === '/register'} >
            Register
          </Menu.Item >
        </Link>
      </>
    )
  };

  return(
    <Menu>
      <Link to='/'>
        <Menu.Item active={location.pathname === '/'} >
          Home
        </Menu.Item >
      </Link>
      <Link to='/profiles'>
        <Menu.Item active={location.pathname === '/profiles'} >
          Launch Profiles
        </Menu.Item >
      </Link>
      <Link to='/plans'>
        <Menu.Item active={location.pathname === '/plans'} >
          Launch Plans
        </Menu.Item >
      </Link>
      <Menu.Menu position="right">{rightNavItems()}</Menu.Menu>
    </Menu>
  );
}

export default withRouter(Navbar)