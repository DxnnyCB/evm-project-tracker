import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'projects' },
  {
    path: 'projects',
    loadComponent: () =>
      import('./features/projects/project-list/project-list.component').then(
        (m) => m.ProjectListComponent,
      ),
  },
  {
    path: 'projects/:projectId',
    loadComponent: () =>
      import('./features/dashboard/project-dashboard/project-dashboard.component').then(
        (m) => m.ProjectDashboardComponent,
      ),
  },
  { path: '**', redirectTo: 'projects' },
];
