function ErrorPage({error}) {
  return (
    <div class="notification is-danger is-light">
      <span class="close"></span>
      Error: {error}
    </div>
  )
}

export default ErrorPage
