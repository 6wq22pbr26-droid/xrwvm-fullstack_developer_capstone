export async function api(path, data) {
 const options={credentials:'same-origin'};
 if(data!==undefined){const c=await fetch('/djangoapp/csrf');const token=(await c.json()).csrfToken;options.method='POST';options.headers={'Content-Type':'application/json','X-CSRFToken':token};options.body=JSON.stringify(data);}
 const res=await fetch('/djangoapp/'+path,options);const json=await res.json();if(!res.ok)throw new Error(json.error||'Request failed. Please try again.');return json;
}
