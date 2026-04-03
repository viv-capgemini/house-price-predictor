{{- define "streamlit.name" -}}
streamlit
{{- end }}

{{- define "streamlit.fullname" -}}
{{ include "streamlit.name" . }}
{{- end }}

{{- define "streamlit.selectorLabels" -}}
app.kubernetes.io/name: {{ include "streamlit.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "streamlit.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{ include "streamlit.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "streamlit.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "streamlit.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
