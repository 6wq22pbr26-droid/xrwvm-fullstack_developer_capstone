import React,{useEffect,useState} from 'react';
import {api} from '../../api';
export default function Header(){const [user,setUser]=useState(null);
 useEffect(()=>{api('session').then(x=>setUser(x.userName)).catch(()=>setUser(null));},[]);
 async function logout(){await api('logout',{});sessionStorage.clear();window.location.href='/';}
 return <header className="site-header"><a className="brand" href="/">Best Cars <span>Dealerships</span></a><nav><a href="/">Home</a><a href="/about">About Us</a><a href="/contact">Contact Us</a>{user?<><strong>{user}</strong><button className="outline" onClick={logout}>Logout</button></>:<><a href="/login">Login</a><a className="button" href="/register">Register</a></>}</nav></header>;
}
