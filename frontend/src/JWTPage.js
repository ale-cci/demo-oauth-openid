import React from 'react'
import jwt from 'jsonwebtoken'
import jwksClient from 'jwks-rsa'

function verifyToken(token, jwksUri) {
  var client = jwksClient({
    jwksUri: jwksUri,
    strictSsl: false,
  });
  function getKey(header, callback){
    console.log(header.kid)
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
      jwt.verify(token, getKey, options,
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

export default function JWTPage({accessToken}) {
  const [secret, setSecret] = React.useState('')
  const [validationError, setValidationError] = React.useState(undefined)
  const [header, setHeader] = React.useState('')
  const [payload, setPayload] = React.useState('')

  React.useEffect(() => {
    const [head, body] = accessToken.split('.')
    setHeader(atob(head))
    setPayload(atob(body))
  }, [accessToken])

  React.useEffect(() => {
    // const [head, body] = accessToken.split('.')
    verifyToken(accessToken, 'http://localhost:4000/oauth/certs')
      .then(_ => setValidationError(undefined))
      .catch(e => setValidationError(e.message))
  }, [accessToken, secret])

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

      {
        validationError === undefined
          ? (
            <div class="field">
              <div class="has-text-success">
                <span class="icon"> <i class="fas fa-check-circle"></i> </span>
                JWT validation successful!
              </div>
            </div>
          )
          : (
            <>
              <div class="field has-text-danger">
                <span class="icon"> <i class="fas fa-exclamation-circle"></i> </span>
                JWT Validation error!
              </div>
              <div class="field notification is-danger is-light">
                {validationError}
              </div>
            </>
          )
      }
    </>
  )
}
