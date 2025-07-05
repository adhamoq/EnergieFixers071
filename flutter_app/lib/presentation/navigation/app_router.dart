import 'package:go_router/go_router.dart';

import '../pages/home_page.dart';
import '../pages/volunteers_page.dart';
import '../pages/visits_page.dart';
import '../pages/appointments_page.dart';
import '../pages/links_page.dart';
import '../pages/settings_page.dart';
import '../widgets/main_layout.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/',
    routes: [
      ShellRoute(
        builder: (context, state, child) {
          return MainLayout(child: child);
        },
        routes: [
          GoRoute(
            path: '/',
            name: 'home',
            builder: (context, state) => const HomePage(),
          ),
          GoRoute(
            path: '/volunteers',
            name: 'volunteers',
            builder: (context, state) => const VolunteersPage(),
          ),
          GoRoute(
            path: '/visits',
            name: 'visits',
            builder: (context, state) => const VisitsPage(),
          ),
          GoRoute(
            path: '/appointments',
            name: 'appointments',
            builder: (context, state) => const AppointmentsPage(),
          ),
          GoRoute(
            path: '/links',
            name: 'links',
            builder: (context, state) => const LinksPage(),
          ),
          GoRoute(
            path: '/settings',
            name: 'settings',
            builder: (context, state) => const SettingsPage(),
          ),
        ],
      ),
    ],
  );
}
