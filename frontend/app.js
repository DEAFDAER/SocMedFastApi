const apiBase = '/'; // same-origin
let currentUser = null;

async function api(path, opts){
  const res = await fetch(apiBase + path, opts);
  return res.json();
}

// signup
document.getElementById('signup-btn').onclick = async ()=>{
  const name = document.getElementById('signup-name').value;
  const age = parseInt(document.getElementById('signup-age').value || '0',10);
  if(!name || !age) return alert('provide name and age');
  const res = await fetch('/persons/', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,age})});
  if(res.ok){
    alert('Created');
  } else {
    const txt = await res.text(); alert('Error: '+txt)
  }
}

// login (name-only)
document.getElementById('login-btn').onclick = ()=>{
  const name = document.getElementById('login-name').value;
  if(!name) return alert('enter name');
  currentUser = name;
  document.getElementById('auth').style.display='none';
  document.getElementById('dashboard').style.display='block';
  document.getElementById('user-name').innerText = name;
  loadFeed();
}

// logout
const logoutBtn = document.getElementById('logout-btn');
if(logoutBtn){
  logoutBtn.onclick = ()=>{
    currentUser = null;
    document.getElementById('auth').style.display='block';
    document.getElementById('dashboard').style.display='none';
    document.getElementById('user-name').innerText = '';
  }
}

// create post
document.getElementById('post-btn').onclick = async ()=>{
  const content = document.getElementById('post-content').value;
  if(!currentUser) return alert('login');
  if(!content) return alert('empty');
  const res = await fetch(`/posts/${encodeURIComponent(currentUser)}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})});
  if(res.ok){
    document.getElementById('post-content').value='';
    loadFeed();
  } else {
    alert('failed to post');
  }
}

async function loadFeed(){
  const feed = document.getElementById('feed');
  feed.innerHTML = '';
  try{
    const res = await fetch('/posts/');
    if(!res.ok){
      const txt = await res.text();
      feed.textContent = 'Error loading posts: ' + txt;
      return;
    }
    const data = await res.json();
    if(!Array.isArray(data)){
      feed.textContent = 'Unexpected response from server';
      console.error('Posts endpoint returned non-array:', data);
      return;
    }
    (data||[]).reverse().forEach(p=>{
      const el = document.createElement('div');
      // show author and a friendly timestamp instead of raw node id
      const header = document.createElement('div');
      header.style.fontWeight = '600';
      const author = p.author_name || 'unknown';
      let time = '';
      try{
        time = p.created_at ? new Date(p.created_at).toLocaleString() : '';
      }catch(e){
        time = p.created_at || '';
      }
      header.textContent = `${author} • ${time}`;

      const content = document.createElement('div');
      content.textContent = p.content || '';
      el.appendChild(header);
      el.appendChild(content);
      el.style.marginTop = '8px';
      feed.appendChild(el);
    })
  }catch(err){
    console.error(err);
    feed.textContent = 'Error loading posts: ' + (err.message || err);
  }
}
