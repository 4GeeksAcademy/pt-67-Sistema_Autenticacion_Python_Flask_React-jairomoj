import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Login = () => {
	const { store, actions } = useContext(Context);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleLogin = (event) => {
		event.preventDefault();
		console.log(actions);
		actions.userLogin(email, password);
	}

	return (
		<div className="text-center mt-5">
			<h1>Login</h1>

			<form className="mx-auto w-50" onSubmit={handleLogin}>
				<input type="email" className="form-control" id="exampleFormControlInput1" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}></input>
				<input type="password" id="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
				<button type="submit" class="btn btn-primary btn-lg">Login</button>
			</form>
		</div>
	);
};
