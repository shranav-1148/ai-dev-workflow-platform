import { useRepositories } from "@/hooks/useRepositories";

export default function DashboardPage() {
  const { data: repos, isLoading, error } = useRepositories();

  if (isLoading) return <div>Loading...</div>;

  if (error) return <div>Error</div>;

  return (
    <div>
      {repos.map((repo: any) => (
        <div key={repo.id}>{repo.name}</div>
      ))}
    </div>
  );
}
