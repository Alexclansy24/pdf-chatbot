export default function TestEnvPage() {
  return (
    <div>
      API URL: {process.env.NEXT_PUBLIC_API_URL}
    </div>
  );
}