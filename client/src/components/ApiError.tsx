import React from 'react';
import { UserError } from '../types/AuthTypes';

export default function ApiError({ errors }: { errors: UserError }) {
  return <div>{errors?.message}</div>;
}
