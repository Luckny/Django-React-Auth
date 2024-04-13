import React from 'react';
import { ValidationError } from '../types/AuthTypes';

export default function ApiError({ errors }: { errors: ValidationError }) {
  let myuniqueidcounter = 0;
  function uniqueId() {
    myuniqueidcounter += 1;
    return myuniqueidcounter;
  }

  return errors ? (
    <div>
      {Object.values(errors).map((errorArray) => (
        <div key={uniqueId()}>
          {errorArray &&
            errorArray.map((error) => <p key={uniqueId()}>{error}</p>)}
        </div>
      ))}
    </div>
  ) : null;
}
