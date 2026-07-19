import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
  ResendConfirmationCodeCommand,
} from "@aws-sdk/client-cognito-identity-provider";
import { jwtDecode } from "jwt-decode";

const CLIENT_ID = import.meta.env.VITE_COGNITO_CLIENT_ID;
const REGION = import.meta.env.VITE_COGNITO_REGION || "us-east-1";

const client = new CognitoIdentityProviderClient({ region: REGION });

// Mirrors Home.py's login(): USER_PASSWORD_AUTH against Cognito, no client secret.
export async function login(username, password) {
  const command = new InitiateAuthCommand({
    ClientId: CLIENT_ID,
    AuthFlow: "USER_PASSWORD_AUTH",
    AuthParameters: {
      USERNAME: username,
      PASSWORD: password,
    },
  });

  const response = await client.send(command);
  const idToken = response.AuthenticationResult.IdToken;

  // Signature is not verified client-side, same as verify_signature=False in the Python app.
  const decodedToken = jwtDecode(idToken);
  const groups = decodedToken["cognito:groups"] || [];

  let group = "UNKNOWN";
  if (groups.includes("supportTeam")) {
    group = "SUPPORT";
  } else if (groups.includes("Users")) {
    group = "CUSTOMER";
  }

  return { group, idToken };
}

// Username is the email, matching the login flow above.
export async function signUp(name, email, password) {
  const command = new SignUpCommand({
    ClientId: CLIENT_ID,
    Username: email,
    Password: password,
    UserAttributes: [
      { Name: "email", Value: email },
      { Name: "name", Value: name },
    ],
  });

  return client.send(command);
}

export async function confirmSignUp(email, code) {
  const command = new ConfirmSignUpCommand({
    ClientId: CLIENT_ID,
    Username: email,
    ConfirmationCode: code,
  });

  return client.send(command);
}

export async function resendConfirmationCode(email) {
  const command = new ResendConfirmationCodeCommand({
    ClientId: CLIENT_ID,
    Username: email,
  });

  return client.send(command);
}
