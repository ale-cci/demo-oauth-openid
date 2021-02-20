import React from 'react'
import jwt from 'jsonwebtoken'
import jwksClient from 'jwks-rsa'

function verifyToken(token, jwksUri) {
  var client = jwksClient({
    jwksUri: jwksUri,
    strictSsl: false,
  });
  function getKey(header, callback){
    client.getSigningKey(header.kid, function(err, key) {
      var signingKey = key.publicKey || key.rsaPublicKey;
      callback(null, signingKey);
    });
  }
  const options = {
    algorithms: ['RS256']
  }

  return new Promise(
    (resolve, reject) => {
      jwt.verify(
        token, getKey, options,
        (err, decoded) => {
          if (err) {
            reject(err)
          } else {
            resolve(decoded)
          }
      })
    }
  )
}

export default function JWTPage({accessToken, authURL}) {
  const [secret, setSecret] = React.useState('')
  const [validationError, setValidationError] = React.useState(undefined)
  const [header, setHeader] = React.useState('')
  const [payload, setPayload] = React.useState('')

  const [tokenURL, setTokenURL] = React.useState('')

  React.useLayoutEffect(() => {
    setTokenURL(authURL + '.well-known/jwks.json')
  }, [authURL])

  React.useEffect(() => {
    if (!accessToken) {
      return
    }
    const [head, body] = accessToken.split('.')
    setHeader(atob(head))
    setPayload(atob(body))
  }, [accessToken])

  React.useEffect(() => {
    // const [head, body] = accessToken.split('.')
    if (!tokenURL) {
      return
    }
    if (!accessToken) {
      setValidationError('accessToken is null')
      return
    }
    verifyToken(accessToken, tokenURL)
      .then(_ => setValidationError(undefined))
      .catch(e => setValidationError(e.message))
  }, [accessToken, secret, tokenURL])

  return (
    <>
      <div className="field">
        <label className="label"> JWT </label>
        <div className="control is-expanded">
          <textarea className="textarea" readOnly value={accessToken} rows="8"/>
        </div>
      </div>

      <div className="columns">
        <div className="column is-half">
          <div className="field">
            <label className="label"> Head </label>
            <div className="control is-expanded">
              <textarea className="textarea" readOnly value={header} rows="5"/>
            </div>
          </div>
        </div>
        <div className="column is-half">
          <div className="field">
            <label className="label"> Body </label>
            <div className="control is-expanded">
              <textarea className="textarea" readOnly value={payload} rows="5"/>
            </div>
          </div>
        </div>
      </div>
      <hr/>

      <div className="field">
        <input className="input" value={tokenURL} onChange={e => setTokenURL(e.target.value)}/>
      </div>

      {
        validationError === undefined
          ? (
            <div className="field">
              <div className="has-text-success">
                <span className="icon"> <i className="fas fa-check-circle"></i> </span>
                JWT validation successful!
              </div>
            </div>
          )
          : (
            <>
              <div className="field has-text-danger">
                <span className="icon"> <i className="fas fa-exclamation-circle"></i> </span>
                JWT Validation error!
              </div>
              <div className="field notification is-danger is-light">
                {validationError}
              </div>
            </>
          )
      }
    </>
  )
}
