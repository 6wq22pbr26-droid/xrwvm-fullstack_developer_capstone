import React,{useEffect,useState} from 'react';
import {api} from '../../api';
export default function Header(){const [user,setUser]=useState(null);const [logoutNotice]=useState(()=>sessionStorage.getItem('logoutNotice')==='1');
 useEffect(()=>{sessionStorage.removeItem('logoutNotice');},[]);
 useEffect(()=>{api('session').then(x=>setUser(x.userName)).catch(()=>setUser(null));},[]);
 async function logout(){await api('logout',{});sessionStorage.clear();sessionStorage.setItem('logoutNotice','1');window.location.href='/';}
 return <><header className="site-header"><a className="brand" href="/">Best Cars <span>Dealerships</span></a><nav><a href="/">Home</a><a href="/about">About Us</a><a href="/contact">Contact Us</a>{user?<><strong>{user}</strong><button className="outline" onClick={logout}>Logout</button></>:<><a href="/login">Login</a><a className="button" href="/register">Register</a></>}</nav></header>{logoutNotice&&<p role="status" style={{margin:'20px 5vw',padding:16,background:'#e0f5e9',color:'#14623e',borderRadius:8}}>You have been successfully logged out.</p>}</>;
}
