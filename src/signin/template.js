/* TEMPLATE SIGN IN */
var yo = require("yo-yo");
var landing = require("../landing/index.js")

var signinForm = yo`<div class="col s12 m7">
                        <div class="row">
                            <div class="signup-box">
                                <h1 class="kmgram">KMERA</h1>
                                <form class="signup-form">
                                <h2>Sign up and share pictures with your friends</h2>
                                <div class="section">
                                    <a class="btn btn-fb hiden-on-small-only">Sign in with Facebook</a>
                                    <a class="btn btn-fb hide-on-med-and-up">Sign in</a>
                                </div>
                                <div class="divider"></div>
                                <div class="section">
                                    <input type="text" name="username" placeholder="User Name">
                                    <input type="password" name="password" placeholder="Password"/>
                                    <button class="btn waves-effect waves-light btn-signup" type="submit">Sign in</button>
                                </div>
                                </form>
                            </div>
                        </div>
                            
                        <div class="row">
                            <div class="login-box">
                                Don't you have an account? <a href="/signup">Enter</a>
                            </div>
                        </div>
                    </div>`;

module.exports = landing(signinForm);
