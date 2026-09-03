# 2026-09 Skill catalog expansion review

## Result

- Existing: 40
- Added unique IDs: 38
- Final: 78
- New APM-selectable: 28
- New operational opt-ins: 10

## Added IDs

- `android-clean-architecture`
- `android-cli`
- `expo-native-ui`
- `compose-multiplatform-patterns`
- `edge-to-edge`
- `expo-api-routes`
- `eas-workflows`
- `expo-deployment`
- `expo-dev-client`
- `expo-module`
- `expo-tailwind-setup`
- `flutter-add-widget-test`
- `flutter-apply-architecture-best-practices`
- `flutter-build-responsive-layout`
- `flutter-fix-layout-issues`
- `flutter-setup-declarative-routing`
- `java-coding-standards`
- `jpa-patterns`
- `kotlin-coroutines-flows`
- `kotlin-patterns`
- `mobile-android-design`
- `mobile-ios-design`
- `expo-data-fetching`
- `navigation-3`
- `nestjs-best-practices`
- `next-cache-components-adoption`
- `nodejs-backend-patterns`
- `r8-analyzer`
- `springboot-patterns`
- `springboot-tdd`
- `sql-optimization-patterns`
- `testing-setup`
- `expo-upgrade`
- `expo-dom`
- `vue-best-practices`
- `vue-router-best-practices`
- `vue-testing-best-practices`
- `web-design-guidelines`

## Alias normalization

- `building-native-ui` -> `expo-native-ui`
- `expo-cicd-workflows` -> `eas-workflows`
- `native-data-fetching` -> `expo-data-fetching`
- `upgrading-expo` -> `expo-upgrade`
- `use-dom` -> `expo-dom`

## Merged or skipped

- `debugging-discipline` -> selected guidance merged into `global/ENGINEERING.md`.
- `engineering-quality` -> already covered by `global/ENGINEERING.md`.
- `springboot-security` -> selected hardening guidance merged into `spring-security`.
- `redis` -> skipped because `redis-core` and `redis-connections` already own the scope.
- Existing same-ID snapshots were not overwritten; upgrades require a separate snapshot review.

## Deferred

`aws`, `azure`, `docker`, `flyway`, `gcp`, `github-actions`, `gitlab-ci`, `jenkins`, `kafka`, `kubernetes`, `mariadb`, `mysql`, and `rabbitmq` remain excluded until immutable source, revision, and license evidence are established.

## Operational isolation

- `android-cli`
- `expo-api-routes`
- `eas-workflows`
- `expo-deployment`
- `expo-dev-client`
- `flutter-fix-layout-issues`
- `next-cache-components-adoption`
- `r8-analyzer`
- `testing-setup`
- `expo-upgrade`

Catalog inclusion is not activation. Ordinary IDs are mirrored under `.apm/skills/`; operational IDs require explicit task authorization.
