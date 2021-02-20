import React from 'react'

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
  const basePath = new URL('http://localhost:4000/oauth')
  basePath.searchParams.append('client_id', 'test')
  basePath.searchParams.append('redirect_uri', 'http://localhost:3000')
  basePath.searchParams.append('scope', 'openid authorizations')
  basePath.searchParams.append('state', 'example')
  return basePath.toString()
}

function RenderDefined({val, label}) {
  return val
    ? <div> {label}: <input value={val}/> </div>
    : <> </>
}

function App() {
  const urlparams = new URLSearchParams(window.location.search)
  const error = urlparams.get('error')
  const accessToken = urlparams.get('access_token')
  const state = urlparams.get('state')
  console.log(accessToken)

  React.useEffect(() => {
    window.localStorage.setItem('jwt', accessToken)
  }, [accessToken])

  const jwt = undefined ; getJWT()

  return (
    <div className="container">
      {
        jwt
          ? <Navigator/>
          : <RequiredLogin sso_provider={ buildURL()}/>
      }
      <div>
        <RenderDefined label="Error" val={error}/>
        <RenderDefined label="AccessToken" val={accessToken}/>
        <RenderDefined label="State" val={state}/>
      </div>
    </div>
  )
}

export default App;
