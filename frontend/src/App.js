import React from 'react'
import ErrorPage from './ErrorPage'
import JWTPage from './JWTPage'

function RequiredLogin({sso_provider}) {
  return (<div> Required <a href={sso_provider}> login </a></div>)
}
function Navigator() {
  return (<div> used logged </div>)
}

function getJWT() {
  return window.localStorage.getItem('jwt')
}

function buildURL(authUrl) {
  const basePath = new URL(authUrl)
  basePath.searchParams.append('client_id', 'test')
  basePath.searchParams.append('redirect_uri', 'http://localhost:3000')
  basePath.searchParams.append('scope', 'openid authorizations')
  basePath.searchParams.append('state', 'example')
  return basePath.toString()
}


function App() {
  const [authURL, setAuthUrl] = React.useState('http://localhost:4000/oauth/')

  const urlparams = new URLSearchParams(window.location.search)
  const error = urlparams.get('error')
  const accessToken = urlparams.get('access_token')
  const state = urlparams.get('state')
  console.log(accessToken)

  React.useEffect(() => {
    window.localStorage.setItem('jwt', accessToken)
  }, [accessToken])

  return (
    <div className="section">
      <div className="container">
        <h1 className="title"> JWT Playground </h1>

        <div className="field has-addons">
          <div className="control is-expanded">
            <input className="input"
              placeholder="http://oauth-endpoint:port/path"
              value={authURL}
              onChange={e => setAuthUrl(e.target.value)}/>
          </div>
          <div className="control">
            <button className="button" onClick={
              () => window.location.href = buildURL(authURL)
              }>
              Go
            </button>
          </div>
        </div>
        <hr/>
        {
          error
            ? <ErrorPage error={error}/>
            : <JWTPage accessToken={accessToken}/>
        }
      </div>
    </div>
  )
}

export default App;
