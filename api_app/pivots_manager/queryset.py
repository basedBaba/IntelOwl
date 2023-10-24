from django.db.models import Q

from api_app.queryset import PythonConfigQuerySet


class PivotConfigQuerySet(PythonConfigQuerySet):
    def valid(
        self, analyzers: PythonConfigQuerySet, connectors: PythonConfigQuerySet
    ) -> "PivotConfigQuerySet":
        qs = self
        if analyzers.exists():
            qs = qs.many_to_many_to_array("related_analyzer_configs").filter(
                Q(
                    related_analyzer_configs_array__contained_by=list(
                        analyzers.values_list("pk", flat=True)
                    )
                )
                | Q(related_analyzer_configs=None)
            )
        if connectors.exists():
            qs = qs.many_to_many_to_array("related_connector_configs").filter(
                Q(
                    related_connector_configs_array__contained_by=list(
                        connectors.values_list("pk", flat=True)
                    )
                )
                | Q(related_connector_configs=None)
            )
        return qs.distinct()
