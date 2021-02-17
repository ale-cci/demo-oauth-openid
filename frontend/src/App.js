function RequiredLogin({sso_provider}) {
  return (<div> Required <a href={sso_provider}> login </a></div>)
}
function Navigator() {
  return (<div> used logged </div>)
}

function getJWT() {
  return window.localStorage.getItem('jwt')
}

function App() {
  const jwt = getJWT()

  return (
    <div className="container">
      {
        jwt
          ? <Navigator/>
          : <RequiredLogin sso_provider="http://localhost:8000/auth"/>
      }
    </div>
  )
}

export default App;
