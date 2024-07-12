import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Signup = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>Signup</h1>
			
			<input type="email" className="form-control" id="exampleFormControlInput1" placeholder="Email"></input>
			<input type="password" id="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" placeholder="Password"></input>
			<button type="button" class="btn btn-primary btn-lg">Signup</button>
		</div>
	);
};
