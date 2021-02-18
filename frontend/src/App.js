function RequiredLogin({sso_provider}) {
  return (<div> Required <a href={sso_provider}> login </a></div>)
}
function Navigator() {
  return (<div> used logged </div>)
}

function getJWT() {
  return window.localStorage.getItem('jwt')
}

function buildURL() {
  const basePath = new URL('http://localhost:8000/oauth')
  basePath.searchParams.append('client_id', 'test')
  basePath.searchParams.append('redirect_uri', 'http://localhost:3000')
  basePath.searchParams.append('scope', 'openid authorizations')
  basePath.searchParams.append('state', '')
  return basePath.toString()
}

function App() {
  const jwt = getJWT()

  return (
    <div className="container">
      {
        jwt
          ? <Navigator/>
          : <RequiredLogin sso_provider={ buildURL()}/>
      }
    </div>
  )
}

export default App;
