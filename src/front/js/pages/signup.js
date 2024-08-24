import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { useNavigate } from "react-router-dom";

export const Signup = () => {
	const { store, actions } = useContext(Context);
	const navigate = useNavigate();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleSignup = (event) => {
		event.preventDefault();
		const success = actions.userSignup(email, password);

		if (success) {
			alert("Usuario creado!");
			navigate('/');
		}
	}

	return (
		<div className="text-center mt-5">
			<h1>Signup</h1>

			<form className="mx-auto w-50" onSubmit={handleSignup}>
				<input type="email" className="form-control" id="exampleFormControlInput1" placeholder="Email" alue={email} onChange={(e) => setEmail(e.target.value)} required></input>
				<input type="password" id="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required></input>
				<button type="submit" class="btn btn-primary btn-lg">Signup</button>
			</form>
		</div>
	);
};
